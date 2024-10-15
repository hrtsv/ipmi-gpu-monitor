import subprocess
import json
from app import db
from app.models import SensorData
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ipmi_sensors(host, username, password):
    cmd = f"ipmitool -H {host} -U {username} -P {password} -I lanplus sdr list full -v -c"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            logger.error(f"IPMI command failed: {result.stderr}")
            return []
        
        sensors = []
        for line in result.stdout.split('\n'):
            if line:
                parts = line.split(',')
                try:
                    sensors.append({
                        'name': parts[0],
                        'type': parts[2],
                        'value': float(parts[3]) if parts[3] != 'na' else None,
                        'unit': parts[4]
                    })
                except (IndexError, ValueError) as e:
                    logger.warning(f"Error parsing sensor data: {e}")
        return sensors
    except subprocess.TimeoutExpired:
        logger.error("IPMI command timed out")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in get_ipmi_sensors: {e}")
        return []

def update_sensor_data():
    try:
        ipmi_sensors = get_ipmi_sensors(Config.IPMI_HOST, Config.IPMI_USERNAME, Config.IPMI_PASSWORD)
        if not ipmi_sensors:
            logger.warning("No IPMI sensor data retrieved")
        
        timestamp = datetime.utcnow()
        
        for sensor in ipmi_sensors:
            if sensor['value'] is not None:
                data = SensorData(timestamp=timestamp, sensor_type='IPMI', sensor_name=sensor['name'], value=sensor['value'])
                db.session.add(data)
        
        db.session.commit()
        logger.info(f"Updated sensor data with {len(ipmi_sensors)} sensors")
    except Exception as e:
        logger.error(f"Error in update_sensor_data: {e}")
        db.session.rollback()

# ... rest of the file remains the same