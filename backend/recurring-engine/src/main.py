from fastapi import FastAPI, Request, Response
from api.recurring_routes import router as recurring_router
from infra.config.validator import load_config_from_env
import uvicorn
import os
import time
from app_logging import logger, log_request
from metrics import record_request_metric

# Load configuration
config = load_config_from_env()

# Create FastAPI app
app = FastAPI(
    title="Recurring Engine Service",
    description="Service for managing recurring tasks in the event-driven architecture",
    version="1.0.0"
)

# Include routers
app.include_router(recurring_router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Add timing header
    response.headers["X-Process-Time"] = str(process_time)
    
    # Record metrics
    record_request_metric(
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )
    
    # Log the request
    log_request(
        request.method,
        request.url.path,
        response.status_code,
        process_time * 1000  # Convert to milliseconds
    )
    
    return response

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "recurring-engine"}

@app.on_event("startup")
async def startup_event():
    print("Recurring Engine Service starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Recurring Engine Service shutting down...")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.host,
        port=int(os.getenv("PORT", 8002)),
        reload=True
    )