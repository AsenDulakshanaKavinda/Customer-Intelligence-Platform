from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_session
from app.database.models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.authentication import get_current_user, create_access_token, verify_password, get_password_hash    

auth_route = APIRouter()

@auth_route.get("/health")
def check_auth_router():
    """
    Health check endpoint for the authentication router. 
    Returns a simple message indicating that the auth route is running. 
    If any error occurs, it raises an HTTP 500 Internal Server Error with the error details.
    """
    try:
        return {
            "message": f"Auth route running...",
            "status_code": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(
            detail=f"Error in auth route: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@auth_route.post("/register")
def register(user: User, db: Session = Depends(get_session)):
    """
    Register a new user. This endpoint checks if the username is already taken, hashes the provided password, and saves the new user to the database. 
    If registration is successful, it returns a success message along with the new user's ID. 
    If any error occurs during registration, it raises an HTTP 500 Internal Server Error with the error details.
    
    args:
    - user: User object containing the username and password for registration.
    - db: Database session dependency for interacting with the database.

    returns:
    - A dictionary containing a success message and the new user's ID if registration is successful.

    exceptions:
    - Raises an HTTP 400 Bad Request if the username is already registered.
    - Raises an HTTP 500 Internal Server Error if any other error occurs during registration.
    """
    try:
        existing_user = db.query(User).filter(User.username == user.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        user.hashed_password = get_password_hash(user.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User registered successfully", "user_id": user.id}
    except Exception as e:
        raise HTTPException(
            detail=f"Error during registration: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@auth_route.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """
    Authenticate a user and generate an access token. This endpoint verifies the provided username and password against the stored credentials. If authentication is successful, it returns an access token and token type. If authentication fails, it raises an HTTP 401 Unauthorized error.
    
    args:
    - form_data: OAuth2PasswordRequestForm containing the username and password for login.
    - db: Database session dependency for interacting with the database.

    returns:
    - A dictionary containing the access token and token type if login is successful.

    exceptions:
    - Raises an HTTP 401 Unauthorized error if the username or password is incorrect.
    - Raises an HTTP 500 Internal Server Error if any other error occurs during login.

    """
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            detail=f"Error during login: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )







