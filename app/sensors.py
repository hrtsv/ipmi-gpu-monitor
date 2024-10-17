import subprocess
import re
from app import db
from app.models import SensorData
from datetime import datetime
import logging
import os

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
        
        if result.returncode != 0:
            logger.error(f"IPMI command failed with return code {result.returncode}")
            return [], []
        
        temperatures = []
        fans = []
        pattern = r'(.*?)\s*\|\s*\w+\s*\|\s*\w+\s*\|\s*[\d.]+\s*\|\s*([\d.]+)\s*(degrees C|RPM)'
        cpu_count = 0
        for line in result.stdout.split('\n'):
            match = re.search(pattern, line)
            if match:
                name = match.group(1).strip()
                value = match.group(2)
                unit = match.group(3)
                try:
                    if unit == 'degrees C':
                        if name == 'Temp':
                            cpu_count += 1
                            name = f'CPU {cpu_count}'
                        temperatures.append({'name': name, 'value': float(value)})
                    elif unit == 'RPM':
                        fans.append({'name': name, 'value': float(value)})
                except ValueError:
                    logger.warning(f"Could not parse value: {value} for sensor: {name}")
        
        logger.debug(f"Parsed IPMI temperatures: {temperatures}")
        logger.debug(f"Parsed IPMI fan speeds: {fans}")
        return temperatures, fans
    except subprocess.TimeoutExpired:
        logger.error("IPMI command timed out")
        return [], []
    except Exception as e:
        logger.error(f"Error fetching IPMI data: {e}")
        return [], []

def update_sensor_data():
    timestamp = datetime.utcnow()
    
    temperatures, fans = get_ipmi_data()
    for temp in temperatures:
        data = SensorData(timestamp=timestamp, sensor_type='Temperature', sensor_name=temp['name'], value=temp['value'])
        db.session.add(data)
    
    for fan in fans:
        data = SensorData(timestamp=timestamp, sensor_type='Fan', sensor_name=fan['name'], value=fan['value'])
        db.session.add(data)
    
    try:
        db.session.commit()
        logger.info(f"Updated sensor data: {len(temperatures)} temperature sensors, {len(fans)} fan sensors")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error committing sensor data to database: {e}")