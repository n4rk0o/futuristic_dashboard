import datetime
from typing import TypedDict


class User(TypedDict):
    id: int
    username: str
    email: str
    hashed_password: str
    created_at: datetime.datetime
    is_active: bool


class OAuth2Token(TypedDict):
    id: int
    user_id: int
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime.datetime
    created_at: datetime.datetime


class OAuth2Client(TypedDict):
    id: int
    client_id: str
    client_secret: str
    redirect_uris: str
    grant_types: str
    scope: str


class OAuth2AuthorizationCode(TypedDict):
    id: int
    user_id: int
    client_id: str
    code: str
    redirect_uri: str
    scope: str
    expires_at: datetime.datetime