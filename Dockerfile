# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install curl and any dependencies
RUN apt-get update && apt-get install -y curl && apt-get clean

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 5000

# Define the command to run your Flask app
CMD ["python", "app.py"]
