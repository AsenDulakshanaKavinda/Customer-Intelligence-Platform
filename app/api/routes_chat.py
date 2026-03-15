from fastapi import APIRouter, status, HTTPException

chat_route = APIRouter()

@chat_route.get("/health")
def check_chat_router():
    try:
        return {
            "message": f"Chat route running...",
            "status_code": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(
            detail=f"Error in chat route: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
 