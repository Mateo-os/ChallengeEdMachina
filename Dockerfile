# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Copy the requirements file into the container
COPY requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the rest of your application code into the container
COPY /app/ /app/

# Expose port 80 for FastAPI
EXPOSE 80

# Command to run your FastAPI application

CMD ["uvicorn", "asgi:app", "--host", "0.0.0.0", "--port", "80"]
