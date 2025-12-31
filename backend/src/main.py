from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.auth_router import auth_router
from .api.todo_router import todo_router
from .database.database import init_db

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(todo_router, prefix="/api/v1", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.on_event("startup")
def on_startup():
    """
    Initialize the database when the application starts.
    """
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)