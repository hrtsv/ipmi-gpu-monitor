# Use an NVIDIA CUDA base image
FROM nvidia/cuda:11.6.2-base-ubuntu20.04

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    ipmitool \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Debugging: List contents of /app
RUN ls -la /app

# Debugging: Print Python version
RUN python3 --version

# Debugging: Cat the generate_secrets.py file
RUN cat generate_secrets.py

# Generate secret keys
RUN python3 generate_secrets.py

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]