# Use an official Python runtime as the base image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (optional but useful for some packages)
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project
COPY . /app/

# Collect static files
RUN python backend/globetrotter_project/manage.py collectstatic --noinput

# Expose a port for local usage (optional if relying on $PORT at runtime)
EXPOSE 8000

# Use $PORT environment variable for Gunicorn, and run migrations first
CMD ["sh", "-c", "python backend/globetrotter_project/manage.py migrate && gunicorn --chdir backend/globetrotter_project --bind 0.0.0.0:$PORT globetrotter_project.wsgi:application"]
