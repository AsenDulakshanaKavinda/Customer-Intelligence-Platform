from fastapi import FastAPI, HTTPException, status


app = FastAPI(
    title="",
    description="",
    docs_url="",
    version=""
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

app.include_router()