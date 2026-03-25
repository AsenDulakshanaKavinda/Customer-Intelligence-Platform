from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

admin_route = APIRouter(dependencies=[Depends(oauth2_scheme)])

@admin_route.get("/health")
def check_admin_router():
    try:
        return {
            "message": f"Admin route running...",
            "status_code": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(
            detail=f"Error in admin route: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
