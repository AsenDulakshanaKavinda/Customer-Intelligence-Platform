from fastapi import APIRouter, status, HTTPException

feedback_route = APIRouter()

@feedback_route.get("/health")
def check_feedback_router():
    try:
        return {
            "message": f"Feedback route running...",
            "status_code": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(
            detail=f"Error in feedback route: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
 