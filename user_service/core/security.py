from datetime import datetime, timedelta, timezone
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from typing import cast
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = cast(timedelta, None)
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", ""))
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    return cast(
        str,
        jwt.encode(
            to_encode, os.environ.get("SECRET_KEY", ""), algorithm=ALGORITHM
        ),
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return cast(bool, pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    return cast(str, pwd_context.hash(password))
