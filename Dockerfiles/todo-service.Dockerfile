FROM python:3.11-slim
WORKDIR /app

# Copy shared dependencies first
COPY backend/shared /app/backend/shared

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the specific service code
COPY backend/todo-service /app/backend/todo-service

# Set PYTHONPATH to include both the service src and the root app directory
ENV PYTHONPATH=/app:/app/backend

# Change to the service directory
WORKDIR /app/backend/todo-service/src

EXPOSE 8001

# Run the service
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]