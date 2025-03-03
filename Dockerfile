# Use an official Python runtime as the base image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy everything from the root directory to /app (this keeps all files)
COPY . /app/

# Set working directory to where manage.py is located
WORKDIR /app/backend/globetrotter_project

# Expose port 8000 for Django
EXPOSE 8000

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
s