from fastapi import APIRouter, HTTPException
from database import find_user_by_email, add_user, users_data
from models.user import User, UserLogin, UserResponse
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

def find_user_by_id(user_id: str):
    """Find user by ID"""
    return next((u for u in users_data if u.get('id') == user_id), None)

# User registration endpoint
@router.post("/register")
async def register(user: User):
    print(f"Registration attempt for email: {user.email}")
    print(f"User data: {user.dict()}")
    
    # Check if email already exists
    existing = find_user_by_email(user.email)
    if existing:
        print(f"Email {user.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")

        # Create new user document
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)  # Simple hash for demo
    user_dict["id"] = str(uuid.uuid4())  # Generate unique user ID
    user_dict["created_at"] = datetime.utcnow().isoformat()  # ← ADD 4 SPACES HERE!
    # Save user to in-memory database
    add_user(user_dict)
# User login endpoint  
@router.post("/login")
async def login(user: UserLogin):
    print(f"Login attempt for email: {user.email}")
    
    # Find user by email
    db_user = find_user_by_email(user.email)
    print(f"User found: {db_user is not None}")

    # Check if user exists and password is correct
    if not db_user:
        print(f"User {user.email} not found")
        raise HTTPException(status_code=400, detail="User not found. Please register first.")
    
    if not verify_password(user.password, db_user["password"]):
        print(f"Invalid password for user {user.email}")
        raise HTTPException(status_code=400, detail="Invalid password")

    # Issue JWT access token
    payload = {"sub": db_user["id"], "email": db_user["email"], "iat": datetime.utcnow()}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    access_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

    print(f"Login successful for user {user.email}")
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": db_user["id"], "email": db_user.get("email"), "username": db_user.get("username")},
    }

# Get user details by ID endpoint
@router.get("/user/{user_id}", response_model=UserResponse)
async def get_user_details(user_id: str):
    """Get user details by user ID"""
    print(f"Fetching details for user ID: {user_id}")
    
    # Find user by ID
    db_user = find_user_by_id(user_id)
    
    if not db_user:
        print(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    print(f"User details found for ID: {user_id}")
    return UserResponse(**db_user)

# Get all users endpoint (for admin purposes)
@router.get("/users")
async def get_all_users():
    """Get all registered users (without passwords)"""
    print("Fetching all users")
    
    # Return all users without passwords
    users_without_passwords = []
    for user in users_data:
        user_copy = user.copy()
        user_copy.pop("password", None)  # Remove password from response
        users_without_passwords.append(user_copy)
    
    return {"users": users_without_passwords, "total": len(users_without_passwords)}