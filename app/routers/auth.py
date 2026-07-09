import json
import os
import secrets
import ssl
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import certifi
from fastapi import APIRouter, Depends, HTTPException, Request as FastAPIRequest
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud
from app.security import hash_password
from app.security import create_access_token
from app.security import get_current_user
from app.models import User
from app.schemas import Token, UserCreate, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
GOOGLE_SCOPE = "openid email profile"
GOOGLE_STATE_COOKIE = "google_oauth_state"


def create_user_token(user: User) -> str:
    return create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "role": user.role
        }
    )


def get_google_redirect_uri() -> str:
    return os.getenv(
        "GOOGLE_REDIRECT_URI",
        "http://127.0.0.1:8000/auth/google/callback"
    )


def get_frontend_redirect_url() -> str:
    return os.getenv(
        "FRONTEND_REDIRECT_URL",
        "http://127.0.0.1:5500/products.html?view=store"
    )


def get_google_config():
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth is not configured"
        )

    return client_id, client_secret


def request_json(url: str, data: dict | None = None, token: str | None = None):
    headers = {}
    body = None

    if data is not None:
        body = urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    if token is not None:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url, data=body, headers=headers)
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    try:
        with urlopen(request, timeout=10, context=ssl_context) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8")

        try:
            detail = json.loads(detail)
        except json.JSONDecodeError:
            pass

        raise HTTPException(
            status_code=400,
            detail=detail
        ) from exc
    except URLError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not connect to Google: {exc.reason}"
        ) from exc


def frontend_redirect_with_token(token: str):
    separator = "&" if "#" in get_frontend_redirect_url() else "#"

    return f"{get_frontend_redirect_url()}{separator}{urlencode({'token': token})}"


def get_or_create_google_user(db: Session, google_user: dict):
    email = google_user.get("email")

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Google account did not return an email"
        )

    user = crud.get_user_by_email(db, email)

    if user:
        return user

    user = User(
        name=google_user.get("name") or email.split("@")[0],
        email=email,
        password=hash_password(secrets.token_urlsafe(32)),
        role="USER"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return crud.create_user(db, user)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = crud.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_user_token(db_user)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/google/login")
def google_login():
    client_id, _ = get_google_config()
    state = secrets.token_urlsafe(32)
    params = {
        "client_id": client_id,
        "redirect_uri": get_google_redirect_uri(),
        "response_type": "code",
        "scope": GOOGLE_SCOPE,
        "state": state,
        "access_type": "online",
        "prompt": "select_account"
    }

    response = RedirectResponse(
        f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    )

    response.set_cookie(
        GOOGLE_STATE_COOKIE,
        state,
        httponly=True,
        samesite="lax",
        max_age=600
    )

    return response


@router.get("/google/callback")
def google_callback(
    request: FastAPIRequest,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    db: Session = Depends(get_db)
):
    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    cookie_state = request.cookies.get(GOOGLE_STATE_COOKIE)

    if not state or state != cookie_state:
        raise HTTPException(
            status_code=401,
            detail="Invalid Google OAuth state"
        )

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Missing Google authorization code"
        )

    client_id, client_secret = get_google_config()
    token_response = request_json(
        GOOGLE_TOKEN_URL,
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": get_google_redirect_uri(),
            "grant_type": "authorization_code"
        }
    )

    google_access_token = token_response.get("access_token")

    if not google_access_token:
        raise HTTPException(
            status_code=400,
            detail="Google did not return an access token"
        )

    google_user = request_json(
        GOOGLE_USERINFO_URL,
        token=google_access_token
    )

    user = get_or_create_google_user(db, google_user)
    access_token = create_user_token(user)
    response = RedirectResponse(frontend_redirect_with_token(access_token))
    response.delete_cookie(GOOGLE_STATE_COOKIE)

    return response


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
