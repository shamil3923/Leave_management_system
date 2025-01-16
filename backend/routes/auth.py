from fastapi import APIRouter, Depends, HTTPException
import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from schemas.employee import User, UserInDB, Token
from datetime import timedelta, datetime
from database import get_db_connection  # Import reusable DB connection
import os 
import sqlite3

auth_router = APIRouter()

# Load environment variables
load_dotenv()

# Constants
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'SECRET_KEY')
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------ Helper Functions ------------------

def verify_password(plain_password, hashed_password):
    """Verify hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hash password securely"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """Generate a JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ------------------ API Routes ------------------

@auth_router.post("/signup", response_model=Token)
async def signup(user: User):
    """Signup API to register a new user"""
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row  # Allow dictionary-like access
        cursor = conn.cursor()
        
        # Check if the email already exists
        cursor.execute("SELECT * FROM users WHERE email = ?", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = get_password_hash(user.password)

        # Add user with default leave balance (e.g., 30 days)
        cursor.execute("INSERT INTO users (name, email, password, leave_balance) VALUES (?, ?, ?, ?)", 
                       (user.name, user.email, hashed_password, 30))
        conn.commit()
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/signin", response_model=Token)
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    """Signin API to authenticate users"""
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Fetch user by email
        cursor.execute("SELECT * FROM users WHERE email = ?", (form_data.username,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not verify_password(form_data.password, user["password"]):  # Use column name instead of index
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
    # Generate JWT token
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
