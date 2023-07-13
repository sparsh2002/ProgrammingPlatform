# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose a port for the Flask application
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Set the command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
