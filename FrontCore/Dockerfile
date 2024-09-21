# Base Image
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd


# Copy the rest of the application code
COPY . .

# Copy the entrypoint script
COPY entrypoint.sh .

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]