from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database_postgres import get_db
from models.user_sql import User
from models.user import User as UserSchema, UserLogin, UserResponse
from datetime import datetime, timedelta
from jose import jwt, JWTError
import os
import uuid

# Create router for authentication endpoints
router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALG = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Simple password hashing (for demo only - in production use proper hashing)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Bcrypt has a maximum password length of 72 bytes
    # Truncate if necessary to prevent errors
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    # Bcrypt has a maximum password length of 72 bytes
    # Truncate if necessary to prevent ValueError
    if isinstance(plain_password, str):
        if len(plain_password.encode('utf-8')) > 72:
            plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(plain_password, hashed_password)


# User registration endpoint
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserSchema, db: Session = Depends(get_db)):
    print(f"Registration attempt for email: {user.email}")
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        print(f"Email {user.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(
        email=user.email,
        username=user.username,
        password=hash_password(user.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "id": new_user.id}

# User login endpoint  
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    print(f"Login attempt for email: {user.email}")
    
    # Find user by email
    db_user = db.query(User).filter(User.email == user.email).first()
    
    # Check if user exists and password is correct
    if not db_user:
        print(f"User {user.email} not found")
        raise HTTPException(status_code=400, detail="User not found. Please register first.")
    
    if not verify_password(user.password, db_user.password):
        print(f"Invalid password for user {user.email}")
        raise HTTPException(status_code=400, detail="Invalid password")

    # Issue JWT access token
    payload = {"sub": str(db_user.id), "email": db_user.email, "iat": datetime.utcnow()}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    access_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

    print(f"Login successful for user {user.email}")
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": str(db_user.id), "email": db_user.email, "username": db_user.username},
    }

# Get user details by ID endpoint
@router.get("/user/{user_id}", response_model=UserResponse)
def get_user_details(user_id: str, db: Session = Depends(get_db)):
    """Get user details by user ID"""
    print(f"Fetching details for user ID: {user_id}")
    
    # Find user by ID
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        print(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=str(db_user.id),
        email=db_user.email,
        username=db_user.username,
        created_at=db_user.created_at
    )

# Get all users endpoint (for admin purposes)
@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    """Get all registered users (without passwords)"""
    users = db.query(User).all()
    
    users_without_passwords = []
    for user in users:
        users_without_passwords.append({
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "created_at": user.created_at,
            "auth_provider": user.auth_provider if hasattr(user, "auth_provider") else "local" 
        })
    
    return {"users": users_without_passwords, "total": len(users_without_passwords)}

# Google OAuth Login/Registration
from google.oauth2 import id_token
from google.auth.transport import requests
from models.user import GoogleLogin

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

@router.post("/google/verify")
def google_auth(login_data: GoogleLogin, db: Session = Depends(get_db)):
    token = login_data.credential
    
    try:
        # Verify the token with Google
        id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        # Get user info from token
        email = id_info.get("email")
        google_id = id_info.get("sub")
        name = id_info.get("name")
        picture = id_info.get("picture")
        
        if not email:
            raise HTTPException(status_code=400, detail="Invalid Google token: Email not found")
            
        print(f"Google login attempt for: {email}")

        # Check if user exists
        db_user = db.query(User).filter(User.email == email).first()
        
        if db_user:
            print(f"User {email} found, updating Google info")
            # Update existing user with Google info if not present
            if not db_user.google_id:
                db_user.google_id = google_id
                db_user.auth_provider = "google"
                db_user.profile_picture = picture
                db.commit()
                db.refresh(db_user)
        else:
            print(f"Creating new user from Google: {email}")
            # Create new user
            new_user = User(
                email=email,
                username=name,
                google_id=google_id,
                auth_provider="google",
                profile_picture=picture,
                password=None # No password for Google users
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            db_user = new_user

        # Create JWT token
        payload = {"sub": str(db_user.id), "email": db_user.email, "iat": datetime.utcnow()}
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.update({"exp": expire})
        access_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(db_user.id), 
                "email": db_user.email, 
                "username": db_user.username,
                "profile_picture": db_user.profile_picture,
                "auth_provider": db_user.auth_provider
            },
        }

    except ValueError as e:
        print(f"Google token verification failed: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid Google token")
    except Exception as e:
        print(f"Google auth error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")
