import subprocess
import json
from app import db
from app.models import SensorData
from datetime import datetime

def get_ipmi_sensors(host, username, password):
    cmd = f"ipmitool -H {host} -U {username} -P {password} sdr list full -v -c"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    sensors = []
    for line in result.stdout.split('\n'):
        if line:
            parts = line.split(',')
            sensors.append({
                'name': parts[0],
                'type': parts[2],
                'value': float(parts[3]) if parts[3] != 'na' else None,
                'unit': parts[4]
            })
    return sensors

def get_nvidia_gpu_info():
    cmd = "nvidia-smi --query-gpu=temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    gpus = []
    for line in result.stdout.split('\n'):
        if line:
            temp, util, mem_used, mem_total = map(float, line.split(','))
            gpus.append({
                'temperature': temp,
                'utilization': util,
                'memory_used': mem_used,
                'memory_total': mem_total
            })
    return gpus

def update_sensor_data():
    ipmi_sensors = get_ipmi_sensors(app.config['IPMI_HOST'], app.config['IPMI_USERNAME'], app.config['IPMI_PASSWORD'])
    gpu_info = get_nvidia_gpu_info()
    
    timestamp = datetime.utcnow()
    
    for sensor in ipmi_sensors:
        if sensor['value'] is not None:
            data = SensorData(timestamp=timestamp, sensor_type='IPMI', sensor_name=sensor['name'], value=sensor['value'])
            db.session.add(data)
    
    for i, gpu in enumerate(gpu_info):
        data = SensorData(timestamp=timestamp, sensor_type='GPU', sensor_name=f'GPU{i}_temp', value=gpu['temperature'])
        db.session.add(data)
        data = SensorData(timestamp=timestamp, sensor_type='GPU', sensor_name=f'GPU{i}_util', value=gpu['utilization'])
        db.session.add(data)
    
    db.session.commit()
