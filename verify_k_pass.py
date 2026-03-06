
import os
import sys

# Add parent directory to path
sys.path.append(os.path.join(os.getcwd(), 'aceit_backend'))

from routes.auth import verify_password

def check_k_password():
    email = "k@gmail.com"
    # Use the specific password the user provided
    password = "karthika"
    # This is the hash I restored earlier
    original_hash = "$2b$12$DOsJRrZYXLK4VsLfVuPGX.acR9FSBTyrOPL1xCFSrfxr9J4TuO68i"
    
    print(f"Testing password '{password}' against hash for {email}")
    
    try:
        is_valid = verify_password(password, original_hash)
        print(f"Verification Result: {is_valid}")
        
    except Exception as e:
        print(f"Error during verification: {e}")

if __name__ == "__main__":
    check_k_password()
