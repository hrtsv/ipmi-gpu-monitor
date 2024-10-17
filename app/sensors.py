import subprocess
import logging
import os
from app import db
from app.models import SensorData
from datetime import datetime
import shutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_ipmi_data():
    # ... (keep the existing get_ipmi_data function as it is)

def get_gpu_temperatures():
    if not shutil.which('nvidia-smi'):
        logger.warning("nvidia-smi not found. GPU monitoring is not available.")
        return []

    try:
        cmd = "nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits"
        logger.debug(f"Executing GPU command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        logger.debug(f"GPU command output: {result.stdout}")
        logger.debug(f"GPU command error: {result.stderr}")
        
        if result.returncode != 0:
            logger.error(f"GPU command failed with return code {result.returncode}")
            return []
        
        temperatures = []
        for i, line in enumerate(result.stdout.split('\n')):
            if line.strip():
                try:
                    temperatures.append({'name': f'GPU {i}', 'value': float(line.strip())})
                except ValueError:
                    logger.warning(f"Could not parse GPU temperature value: {line.strip()} for GPU {i}")
        
        logger.debug(f"Parsed GPU temperatures: {temperatures}")
        return temperatures
    except subprocess.TimeoutExpired:
        logger.error("GPU command timed out")
        return []
    except Exception as e:
        logger.error(f"Error fetching GPU temperatures: {e}")
        return []

def update_sensor_data():
    timestamp = datetime.utcnow()
    
    temperatures, fans = get_ipmi_data()
    for temp in temperatures:
        data = SensorData(timestamp=timestamp, sensor_type='Temperature', sensor_name=temp['name'], value=temp['value'])
        db.session.add(data)
    
    for fan in fans:
        data = SensorData(timestamp=timestamp, sensor_type='Fan', sensor_name=fan['name'], value=fan['value'])
        db.session.add(data)
    
    gpu_temps = get_gpu_temperatures()
    for temp in gpu_temps:
        data = SensorData(timestamp=timestamp, sensor_type='Temperature', sensor_name=temp['name'], value=temp['value'])
        db.session.add(data)
    
    try:
        db.session.commit()
        logger.info(f"Updated sensor data: {len(temperatures)} temperature sensors, {len(fans)} fan sensors, {len(gpu_temps)} GPU temperature sensors")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error committing sensor data to database: {e}")

    if not gpu_temps:
        logger.info("No GPU temperature data available. Make sure NVIDIA drivers and nvidia-smi are installed if you have NVIDIA GPUs.")