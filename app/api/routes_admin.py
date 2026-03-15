from fastapi import APIRouter, status, HTTPException

admin_route = APIRouter()

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
 