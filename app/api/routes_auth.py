from fastapi import APIRouter, status, HTTPException

auth_route = APIRouter()

@auth_route.get("/health")
def check_auth_router():
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
 