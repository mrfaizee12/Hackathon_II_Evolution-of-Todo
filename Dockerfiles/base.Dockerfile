FROM python:3.11-slim

WORKDIR /app

# Copy shared dependencies
COPY backend/shared /app/backend/shared

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy common configurations
COPY backend/infra /app/backend/infra

# Common health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:$PORT/health || exit 1