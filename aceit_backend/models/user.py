from pydantic import BaseModel
from datetime import datetime

# Simplified user model without email validation
class User(BaseModel):
    username: str
    email: str  # Simple string instead of EmailStr
    password: str

class UserLogin(BaseModel):
    email: str  # Simple string instead of EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime