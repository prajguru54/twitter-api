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
from jose import jwt
from user_service.core import constants
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: Dict[str, Any], access_token_expires_minutes: timedelta
) -> str:
    expire_at = datetime.now(timezone.utc) + access_token_expires_minutes
    to_encode = data.copy()
    to_encode["expire_at"] = expire_at.isoformat()
    return jwt.encode(
        to_encode, key=os.environ["SECRET_KEY"], algorithm=constants.ALGORITHM
    )


@router.post("/token", response_model=schemas.Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(dependencies.get_db),
):
    print("Login user")
    user = crud_user.get_by_email(db, form_data.username)
    print(f"User: {user}")
    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires_minutes = timedelta(
        minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        {"sub": str(user.id)}, access_token_expires_minutes
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/", response_model=schemas.UserResponse)
def create_user(
    *, db: Session = Depends(dependencies.get_db), user_in: schemas.UserCreate
):
    if _ := crud_user.get_by_email(db, user_in.email):
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )
    return crud_user.create(db, user_in)


@router.get("/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(dependencies.get_db)):
    return crud_user.get_multi(db)


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user_by_id(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: Annotated[int, Path(title="The ID of the user to get", gt=0)],
    current_user: Annotated[
        schemas.UserInDB, Depends(dependencies.get_current_user)
    ],
):
    if current_user.id != user_id:
        return unauthorized_exception
    return crud_user.get(db, user_id)


@router.put("/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    *,
    current_user: Annotated[
        schemas.UserInDB, Depends(dependencies.get_current_user)
    ],
    db: Session = Depends(dependencies.get_db),
    user_id: Annotated[int, Path(title="The ID of the user to update", gt=0)],
    user_in: schemas.UserUpdate,
):
    print(f"==========user_in========: {user_in.model_dump()}")
    if user := crud_user.get(db, user_id):
        return crud_user.update(db=db, db_obj=user, obj_in=user_in)
    else:
        raise HTTPException(status_code=404, detail="User doesn't exist")


@router.delete("/{user_id}", response_model=schemas.UserResponse)
async def delete_user(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: Annotated[int, Path(title="The ID of the user to update", gt=0)],
):
    if _ := crud_user.get(db, user_id):
        return crud_user.remove(db=db, id=user_id)
    else:
        raise HTTPException(status_code=404, detail="User doesn't exist")
