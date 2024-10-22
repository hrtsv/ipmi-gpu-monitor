FROM nvidia/cuda:11.6.2-base-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_RUN_HOST=0.0.0.0

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    ipmitool \
    tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages directly
RUN pip3 install --no-cache-dir \
    Flask==2.0.3 \
    Werkzeug==2.0.3 \
    Flask-SQLAlchemy==2.5.1 \
    Flask-JWT-Extended==4.3.1 \
    SQLAlchemy==1.3.24 \
    gunicorn==20.1.0 \
    python-dotenv==0.19.2

# Verify JWT package installation
RUN python3 -c "from flask_jwt_extended import JWTManager; print('JWT package successfully installed')"

# Copy application code
COPY app ./app
COPY run.py .

# Create data directory
RUN mkdir -p /app/data

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "1", "--timeout", "120", "run:app"]