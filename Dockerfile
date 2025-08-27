# Start from a Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DOCKER_CONTAINER=True

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for mysqlclient and other packages
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    mariadb-client-compat \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create directory for static files
RUN mkdir -p /app/staticfiles

# Copy and make entrypoint script executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port the app runs on
EXPOSE 8006

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8006", "--workers", "3", "--timeout", "120", "alkosto_verify.wsgi:application"]