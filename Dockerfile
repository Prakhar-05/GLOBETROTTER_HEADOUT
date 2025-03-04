# Use an official Python runtime as the base image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (optional but useful for some packages)
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies in a virtual environment
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files after installing dependencies
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

CMD ["gunicorn", "--chdir", "backend/globetrotter_project", "--bind", "0.0.0.0:8000", "globetrotter_project.wsgi:application"]

