from pydantic import BaseModel
from datetime import datetime

# Simplified user model without email validation
class User(BaseModel):
    username: str
    email: str  # Simple string instead of EmailStr
    password: str = None # Optional for OAuth users

class UserLogin(BaseModel):
    email: str  # Simple string instead of EmailStr
    password: str

class GoogleLogin(BaseModel):
    credential: str # Google ID token

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    profile_picture: str = None
    auth_provider: str = "local"
    created_at: datetime