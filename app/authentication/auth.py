import os
from dotenv import load_dotenv; load_dotenv()

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_session
from app.database.models import User

from app.utils import get_logger, cfg
log = get_logger(__file__)

# configurations for JWT
SECRET_KEY = os.getenv(cfg.authentication.SECRET_KEY)
ALGORITHM = os.getenv(cfg.authentication.ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv(cfg.authentication.ACCESS_TOKEN_EXPIRE_MINUTES))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    """Verify a plain password against its hashed version."""
    try:
        log.info("Verifying password")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        log.error(f"Error verifying password: {str(e)}")
        return False    
    
def get_password_hash(password):
    """Hash a plain password using bcrypt."""
    try:
        log.info("Hashing password")
        return pwd_context.hash(password)
    except Exception as e:
        log.error(f"Error hashing password: {str(e)}")
        raise RuntimeError("Password hashing failed")
    
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token with an optional expiration time."""
    try:
        log.info("Creating access token")
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        log.error(f"Error creating access token: {str(e)}")
        raise RuntimeError("Access token creation failed")

def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    """
    Get the current user based on the provided JWT token. This function decodes the token, 
    retrieves the username, and fetches the corresponding user from the database. 
    If any step fails, it raises an HTTP 401 Unauthorized exception.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise credentials_exception
    return user








