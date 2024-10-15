# Use an NVIDIA CUDA base image with Python 3.9
FROM nvidia/cuda:11.6.2-base-ubuntu20.04

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-dev \
    python3-pip \
    build-essential \
    ipmitool \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN python3.9 -m pip install --no-cache-dir --upgrade pip setuptools

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["python3.9", "-m", "flask", "run", "--host=0.0.0.0"]