FROM python:3.11-slim

WORKDIR /app

# Copy shared dependencies
COPY backend/shared /app/backend/shared

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the specific service code
COPY backend/chatbot-service /app/backend/chatbot-service

# Set PYTHONPATH to include both the root app directory and the service src
ENV PYTHONPATH=/app:/app/backend

# Expose port
EXPOSE 8004

# Run the service
CMD ["sh", "-c", "uvicorn backend.chatbot-service.src.main:app --host 0.0.0.0 --port $PORT"]