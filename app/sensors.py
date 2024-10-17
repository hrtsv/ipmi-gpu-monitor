import subprocess
import re
from app import db
from app.models import SensorData
from datetime import datetime
import logging
import os
import shutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_ipmi_temperatures():
    try:
        ipmi_host = os.environ.get('IPMI_HOST')
        ipmi_user = os.environ.get('IPMI_USERNAME')
        ipmi_pass = os.environ.get('IPMI_PASSWORD')
        cmd = f"ipmitool -H {ipmi_host} -U {ipmi_user} -P {ipmi_pass} -I lanplus sdr type temperature"
        logger.debug(f"Executing IPMI command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        logger.debug(f"IPMI command output: {result.stdout}")
        logger.debug(f"IPMI command error: {result.stderr}")
        
        if result.returncode != 0:
            logger.error(f"IPMI command failed with return code {result.returncode}")
            return []
        
        temperatures = []
        pattern = r'(.*?)\s*\|\s*\w+\s*\|\s*\w+\s*\|\s*[\d.]+\s*\|\s*([\d.]+)\s*degrees C'
        for line in result.stdout.split('\n'):
            match = re.search(pattern, line)
            if match:
                name = match.group(1).strip()
                value = match.group(2)
                try:
                    temperatures.append({'name': name, 'value': float(value)})
                except ValueError:
                    logger.warning(f"Could not parse temperature value: {value} for sensor: {name}")
        
        logger.debug(f"Parsed IPMI temperatures: {temperatures}")
        return temperatures
    except subprocess.TimeoutExpired:
        logger.error("IPMI command timed out")
        return []
    except Exception as e:
        logger.error(f"Error fetching IPMI temperatures: {e}")
        return []

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
    
    ipmi_temps = get_ipmi_temperatures()
    for temp in ipmi_temps:
        data = SensorData(timestamp=timestamp, sensor_type='IPMI', sensor_name=temp['name'], value=temp['value'])
        db.session.add(data)
    
    gpu_temps = get_gpu_temperatures()
    for temp in gpu_temps:
        data = SensorData(timestamp=timestamp, sensor_type='GPU', sensor_name=temp['name'], value=temp['value'])
        db.session.add(data)
    
    try:
        db.session.commit()
        logger.info(f"Updated sensor data: {len(ipmi_temps)} IPMI sensors, {len(gpu_temps)} GPU sensors")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error committing sensor data to database: {e}")