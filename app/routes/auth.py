from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate,UserLogin
from app.core.security import (hash_password,verify_password,create_access_token,create_refresh_token,SECRET_KEY,ALGORITHM)
from jose import jwt,JWTError

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User registered successfully"
    }
@router.post("/login")
def login(
    form_data:OAuth2PasswordRequestForm=Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": db_user.email,
         "role": db_user.role}
    )
    refresh_token=create_refresh_token({"sub":db_user.email,"role":db_user.role})
    return {
        "access_token": access_token,
        "refresh_token":refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        access_token = create_access_token(
            {"sub": email}
        )

        return {
            "access_token": access_token
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )