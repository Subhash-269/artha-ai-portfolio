## Multi-stage build: React frontend + Django backend in one service

# Stage 1: build React app
FROM node:18-alpine AS frontend-build

WORKDIR /frontend

# Install dependencies and build the React app
COPY front_end/package.json front_end/package-lock.json* ./
RUN npm install
COPY front_end/ .
RUN npm run build


# Stage 2: Python/Django backend serving API and built frontend
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies for scientific Python stack
RUN apt-get update \ 
    && apt-get install -y --no-install-recommends build-essential \ 
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

# Install Python dependencies plus gunicorn for production serving
RUN pip install --no-cache-dir -r requirements.txt gunicorn==21.2.0

# Copy Django project (including entrypoint.sh)
COPY . .

# Copy built React app into Django app directory
COPY --from=frontend-build /frontend/build ./front_end/build

ENV PORT=8000

# Ensure entrypoint script is executable and run it on container start
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
