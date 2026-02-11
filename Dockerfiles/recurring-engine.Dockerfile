FROM python:3.11-slim

WORKDIR /app

# Copy shared dependencies
COPY backend/shared /app/backend/shared

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the specific service code
COPY backend/recurring-engine /app/backend/recurring-engine

# Set PYTHONPATH to include both the root app directory and the service src
ENV PYTHONPATH=/app:/app/backend

# Expose port
EXPOSE 8002

# Run the service
CMD ["sh", "-c", "uvicorn backend.recurring-engine.src.main:app --host 0.0.0.0 --port $PORT"]