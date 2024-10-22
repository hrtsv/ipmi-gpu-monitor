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
    try:
        ipmi_host = os.environ.get('IPMI_HOST')
        ipmi_user = os.environ.get('IPMI_USERNAME')
        ipmi_pass = os.environ.get('IPMI_PASSWORD')
        cmd = f"ipmitool -H {ipmi_host} -U {ipmi_user} -P {ipmi_pass} -I lanplus sdr"
        logger.debug(f"Executing IPMI command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        logger.debug(f"IPMI command output: {result.stdout}")
        logger.debug(f"IPMI command error: {result.stderr}")
        
        temperatures = []
        fans = []
        cpu_count = 0
        for line in result.stdout.split('\n'):
            parts = line.split('|')
            if len(parts) >= 3:
                name = parts[0].strip()
                value_str = parts[1].strip()
                status = parts[2].strip()
                
                if 'degrees C' in value_str:
                    try:
                        value = float(value_str.split()[0])
                        if name == 'Temp':
                            cpu_count += 1
                            name = f'CPU {cpu_count}'
                        temperatures.append({'name': name, 'value': value})
                    except ValueError:
                        logger.warning(f"Could not parse temperature value: {value_str} for sensor: {name}")
                elif 'RPM' in value_str:
                    try:
                        value = float(value_str.split()[0])
                        fans.append({'name': name, 'value': value})
                    except ValueError:
                        logger.warning(f"Could not parse fan speed value: {value_str} for sensor: {name}")
        
        logger.debug(f"Parsed IPMI temperatures: {temperatures}")
        logger.debug(f"Parsed IPMI fan speeds: {fans}")
        return temperatures, fans
    except subprocess.TimeoutExpired:
        logger.error("IPMI command timed out")
        return [], []
    except Exception as e:
        logger.error(f"Error fetching IPMI data: {e}")
        return [], []

def get_gpu_temperatures():
    if not shutil.which('nvidia-smi'):
        logger.info("nvidia-smi not found. GPU monitoring is disabled.")
        return []

    try:
        cmd = "nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits"
        logger.debug(f"Executing GPU command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            logger.warning("GPU command failed. GPU monitoring is disabled.")
            return []
        
        temperatures = []
        for i, line in enumerate(result.stdout.split('\n')):
            if line.strip():
                try:
                    temperatures.append({'name': f'GPU {i}', 'value': float(line.strip())})
                except ValueError:
                    logger.warning(f"Could not parse GPU temperature value: {line.strip()} for GPU {i}")
        
        return temperatures
    except Exception as e:
        logger.warning(f"Error fetching GPU temperatures: {e}")
        return []

def update_sensor_data():
    try:
        timestamp = datetime.utcnow()
        
        temperatures, fans = get_ipmi_data()
        
        # Store temperature data
        for temp in temperatures:
            data = SensorData(
                timestamp=timestamp,
                sensor_type='Temperature',
                sensor_name=temp['name'],
                value=temp['value']
            )
            db.session.add(data)
        
        # Store fan data
        for fan in fans:
            data = SensorData(
                timestamp=timestamp,
                sensor_type='Fan',
                sensor_name=fan['name'],
                value=fan['value']
            )
            db.session.add(data)
        
        # Try to get GPU data if available
        gpu_temps = get_gpu_temperatures()
        for temp in gpu_temps:
            data = SensorData(
                timestamp=timestamp,
                sensor_type='Temperature',
                sensor_name=temp['name'],
                value=temp['value']
            )
            db.session.add(data)
        
        db.session.commit()
        logger.info(f"Updated sensor data: {len(temperatures)} temperature sensors, {len(fans)} fan sensors, {len(gpu_temps)} GPU temperature sensors")
        
    except Exception as e:
        logger.error(f"Error in update_sensor_data: {e}")
        db.session.rollback()