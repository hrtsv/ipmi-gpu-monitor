import subprocess
from app.sensors import get_ipmi_sensors, get_nvidia_gpu_info

def set_fan_speed(host, username, password, fan_id, speed):
    cmd = f"ipmitool -H {host} -U {username} -P {password} raw 0x30 0x30 0x02 0xff {fan_id} {speed}"
    subprocess.run(cmd, shell=True)

def adjust_fan_speed(host, username, password):
    ipmi_sensors = get_ipmi_sensors(host, username, password)
    gpu_info = get_nvidia_gpu_info()
    
    cpu_temp = max([s['value'] for s in ipmi_sensors if s['type'] == 'Temperature' and 'CPU' in s['name']], default=0)
    gpu_temp = max([gpu['temperature'] for gpu in gpu_info], default=0)
    
    max_temp = max(cpu_temp, gpu_temp)
    
    if max_temp < 50:
        fan_speed = 20
    elif max_temp < 60:
        fan_speed = 40
    elif max_temp < 70:
        fan_speed = 60
    elif max_temp < 80:
        fan_speed = 80
    else:
        fan_speed = 100
    
    # Assuming we have 4 fans, adjust as needed
    for fan_id in range(4):
        set_fan_speed(host, username, password, fan_id, fan_speed)

    return fan_speed
