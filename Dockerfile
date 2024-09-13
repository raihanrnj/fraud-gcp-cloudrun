# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8080 to match the Cloud Run requirements
EXPOSE 8080

# Command to run the app (Gunicorn is a production-grade WSGI HTTP server)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
