from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.auth_router import auth_router
from .api.todo_router import todo_router
from .api.v1.chat_router import router as chat_router
from .database.database import init_db

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Allow local frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(todo_router, prefix="/api/v1", tags=["todos"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])  # Include the new chat router

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