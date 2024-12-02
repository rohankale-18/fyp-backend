from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .auth.routes import router as auth_router
from .dashboard.routes import router as dashboard_router

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Custom error handler for unhandled exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    print(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."}
    )

# Include the routers for auth and kanban
app.include_router(auth_router, prefix="/fyp", tags=["auth"])
app.include_router(dashboard_router, prefix="/fyp", tags=["dashboard"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Generator Maintenance!"}
