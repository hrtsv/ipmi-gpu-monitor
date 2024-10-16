import subprocess
import json
from app import db
from app.models import SensorData
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_ipmi_temperatures():
    try:
        cmd = f"ipmitool -H {os.environ.get('IPMI_HOST')} -U {os.environ.get('IPMI_USERNAME')} -P {os.environ.get('IPMI_PASSWORD')} sdr type temperature"
        logger.debug(f"Executing IPMI command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        logger.debug(f"IPMI command output: {result.stdout}")
        logger.debug(f"IPMI command error: {result.stderr}")
        temperatures = []
        for line in result.stdout.split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) >= 3:
                    name = parts[0].strip()
                    value = parts[1].strip().split()[0]
                    temperatures.append({'name': name, 'value': float(value)})
        logger.debug(f"Parsed IPMI temperatures: {temperatures}")
        return temperatures
    except Exception as e:
        logger.error(f"Error fetching IPMI temperatures: {e}")
        return []

def get_gpu_temperatures():
    try:
        cmd = "nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits"
        logger.debug(f"Executing GPU command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        logger.debug(f"GPU command output: {result.stdout}")
        logger.debug(f"GPU command error: {result.stderr}")
        temperatures = []
        for i, line in enumerate(result.stdout.split('\n')):
            if line.strip():
                temperatures.append({'name': f'GPU {i}', 'value': float(line.strip())})
        logger.debug(f"Parsed GPU temperatures: {temperatures}")
        return temperatures
    except Exception as e:
        logger.error(f"Error fetching GPU temperatures: {e}")
        return []

def update_sensor_data():
    timestamp = datetime.utcnow()
    
    ipmi_temps = get_ipmi_temperatures()
    for temp in ipmi_temps:
        data = SensorData(timestamp=timestamp, sensor_type='IPMI', sensor_name=temp['name'], value=temp['value'])
        db.session.add(data)
    
    gpu_temps = get_gpu_temperatures()
    for temp in gpu_temps:
        data = SensorData(timestamp=timestamp, sensor_type='GPU', sensor_name=temp['name'], value=temp['value'])
        db.session.add(data)
    
    db.session.commit()
    logger.info(f"Updated sensor data: {len(ipmi_temps)} IPMI sensors, {len(gpu_temps)} GPU sensors")