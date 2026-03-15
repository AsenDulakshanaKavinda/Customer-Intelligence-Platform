from fastapi import FastAPI, HTTPException, status
from .routes_admin import admin_route
from .routes_chat import chat_route
from .routes_feedback import feedback_route


app = FastAPI(
    title="ex name",
    description="ex desc",
    docs_url="/docs",
    version="n"
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

app.include_router(router=admin_route, prefix="/admin")
app.include_router(router=chat_route, prefix="/chat")
app.include_router(router=feedback_route, prefix="/feedback")
