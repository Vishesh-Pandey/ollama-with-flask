# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && apt-get clean

# Install ollama CLI
RUN curl -fsSL https://ollama.ai/install.sh | bash

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Install the llama:3.2:1b model
RUN ollama pull llama3.2:1b

# Expose the Flask application port
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
