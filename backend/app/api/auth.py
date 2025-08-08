from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import hash_password, verify_password, create_access_token
from ..models.user import User
from ..schemas.auth import UserRegistration, UserLogin, UserResponse, Token


# create router
router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED
             )
def register_user(
    user_data: UserRegistration,
    db: Session = Depends(get_db)
):
    """
    Register a new user account
    1. Validates input data
    2. Checks if email already exists
    3. Hashes password
    4. Creates user in db
    5. Returns user info
    """
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registers"
        )
    
    # hash password
    hashed_password = hash_password(user_data.password)

    # create new user
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        birth_date=user_data.birth_date,
        timezone=user_data.timezone
    )

    # Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    """
        Login Existing User
    """
    # Validate Username
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    # Create access token
    access_token = create_access_token(subject=str(user.id))

    return Token(access_token=access_token)



    
