import subprocess
import logging
import os
from app import db
from app.models import SensorData, SensorThreshold
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

def adjust_fan_speeds():
    """
    Adjust fan speeds based on current temperature readings and thresholds.
    """
    try:
        # Fetch the latest temperature readings
        temperatures = SensorData.query.filter_by(sensor_type='Temperature').order_by(SensorData.timestamp.desc()).all()
        
        # Fetch the threshold settings for each sensor
        thresholds = {t.sensor_name: t for t in SensorThreshold.query.all()}
        
        fan_adjustments = {}

        for temp in temperatures:
            sensor_name = temp.sensor_name
            sensor_value = temp.value

            # Get the corresponding threshold for the sensor
            threshold = thresholds.get(sensor_name)
            if threshold:
                # Adjust fan speeds based on temperature readings and thresholds
                if sensor_value > threshold.max_value:
                    # Temperature is too high, increase fan speed
                    fan_speed = min(100, (sensor_value - threshold.max_value) * 2)  # Example logic
                elif sensor_value < threshold.min_value:
                    # Temperature is too low, decrease fan speed
                    fan_speed = max(10, (threshold.min_value - sensor_value) * 2)  # Example logic
                else:
                    # Keep fan at a moderate speed
                    fan_speed = 50

                # Store the adjusted fan speed
                fan_adjustments[sensor_name] = fan_speed

        # Apply fan adjustments to the database or external hardware (IPMI)
        for sensor_name, fan_speed in fan_adjustments.items():
            logger.info(f"Adjusting fan speed for {sensor_name} to {fan_speed}%")
            update_fan_speed(sensor_name, fan_speed)  # Function to update fan speeds

    except Exception as e:
        logger.error(f"Error in adjust_fan_speeds: {e}")

def update_fan_speed(sensor_name, speed):
    # Example placeholder for actual hardware fan control logic (IPMI or similar)
    logger.info(f"Updating fan speed for {sensor_name} to {speed}%")
    # Use IPMI commands to control fans based on the sensor name and desired speed

def update_sensor_data():
    """
    Fetch IPMI and GPU sensor data, store it in the database, and adjust fan speeds accordingly.
    """
    try:
        timestamp = datetime.utcnow()
        
        # Fetch data from IPMI sensors
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
        
        # Commit data to the database
        db.session.commit()

        # Adjust fan speeds based on sensor data
        adjust_fan_speeds()

        logger.info(f"Updated sensor data: {len(temperatures)} temperature sensors, {len(fans)} fan sensors, {len(gpu_temps)} GPU temperature sensors")
        
    except Exception as e:
        logger.error(f"Error in update_sensor_data: {e}")
        db.session.rollback()
