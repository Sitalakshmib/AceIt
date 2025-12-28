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
def hash_password(password: str) -> str:
    # Simple reversible hash for demo - NOT for production!
    return f"hashed_{password}"

def verify_password(plain_password, hashed_password):
    # Simple verification for demo
    return hashed_password == f"hashed_{plain_password}"

# User registration endpoint
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserSchema, db: Session = Depends(get_db)):
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
async def login(user: UserLogin, db: Session = Depends(get_db)):
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
async def get_user_details(user_id: str, db: Session = Depends(get_db)):
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
async def get_all_users(db: Session = Depends(get_db)):
    """Get all registered users (without passwords)"""
    users = db.query(User).all()
    
    users_without_passwords = []
    for user in users:
        users_without_passwords.append({
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "created_at": user.created_at
        })
    
    return {"users": users_without_passwords, "total": len(users_without_passwords)}
