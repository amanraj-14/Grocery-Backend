import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallbacksecret123")
ALGORITHM = "HS256"

# Safety check
if not SECRET_KEY:
    raise Exception("❌ SECRET_KEY missing in .env file")

# 🔐 Hash password (Using direct bcrypt)
def hash_password(password: str):
    # Password ko bytes mein convert karna padta hai
    pwd_bytes = password.encode('utf-8')
    # Salt generate karke hash banana
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')  # Database ke liye wapas string mein convert kiya

# 🔍 Verify password
def verify_password(plain: str, hashed: str):
    try:
        return bcrypt.checkpw(
            plain.encode('utf-8'), 
            hashed.encode('utf-8')
        )
    except Exception:
        return False

# 🎟️ Create JWT token (Ye same rahega)
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=2)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)