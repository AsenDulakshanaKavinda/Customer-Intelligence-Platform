from fastapi import FastAPI, HTTPException, status
from .routes_admin import admin_route
from .routes_chat import chat_route
from .routes_feedback import feedback_route
from .routes_auth import auth_route


app = FastAPI(
    title="Customer Intelligence Platform API",
    description="API for managing customer interactions, feedback, and insights. " \
    "This API provides endpoints for authentication, chat management, feedback collection, and administrative tasks.",
    docs_url="/docs",
    version="n"
)

@app.get("/")
def home():
    try:
        return {
            "title": "Customer Intelligence Platform API",
            "description": "API for managing customer interactions, feedback, and insights. "\
            "This API provides endpoints for authentication, chat management, feedback collection, and administrative tasks.",
            "status_code": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(
            detail=f"Error: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.get("/health")
def check_health():
    try:
        return {
            "message": f"API running...",
            "status_code": status.HTTP_200_OK
        }
    except Exception as e:
        raise HTTPException(
            detail=f"Error: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

app.include_router(router=auth_route, prefix="/auth")
app.include_router(router=admin_route, prefix="/admin")
app.include_router(router=chat_route, prefix="/chat")
app.include_router(router=feedback_route, prefix="/feedback")
