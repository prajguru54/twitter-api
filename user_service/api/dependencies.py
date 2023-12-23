from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from user_service.core import security
from user_service.models import User
from user_service import schemas
from user_service.core.db.db_conf import session
from user_service.crud import crud_user
import os
from datetime import timezone
from fastapi import APIRouter, Depends, HTTPException, Path, status
from user_service import schemas
from sqlalchemy.orm import Session
from user_service.api import dependencies
from user_service.crud import crud_user
from typing import Annotated, Dict, Any
from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()


ACCESS_TOKEN_EXPIRE_MINUTES = 5
SECRET_KEY = "secret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{os.environ.get('API_V1_STR', '')}/login/access-token"
)

unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_db() -> Generator:
    try:
        db = session
        yield db
    finally:
        db.close()


# def get_current_user(
#     db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
# ) -> User:  # sourcery skip: raise-from-previous-error
#     try:
#         payload = jwt.decode(
#             token,
#             os.environ.get("SECRET_KEY", ""),
#             algorithms=[security.ALGORITHM],
#         )
#         token_data = schemas.TokenPayload(**payload)
#     except (JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     if user := crud_user.get(db, id=token_data.sub):
#         return user
#     else:
#         raise HTTPException(status_code=404, detail="User not found")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(dependencies.get_db),
):
    print(f"Token: {token}")
    try:
        decoded_token = jwt.decode(
            token, key=SECRET_KEY, algorithms=[ALGORITHM]
        )
        print(f"Decoded token: {decoded_token}")
        user_id = decoded_token.get("sub", "")
        print(f"user id: {user_id}")
        if not user_id:
            raise unauthorized_exception
    except JWTError as e:
        raise unauthorized_exception from e
    if user := crud_user.get(db, user_id):
        return user
    else:
        raise unauthorized_exception


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
