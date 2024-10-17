from flask import Blueprint, jsonify, request, render_template
from app.models import SensorData
from app import db
from app.sensors import update_sensor_data
import logging

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/temperatures')
def get_temperatures():
    try:
        update_sensor_data()  # Update sensor data before fetching
        ipmi_temps = SensorData.query.filter_by(sensor_type='IPMI').order_by(SensorData.timestamp.desc()).limit(10).all()
        gpu_temps = SensorData.query.filter_by(sensor_type='GPU').order_by(SensorData.timestamp.desc()).limit(10).all()
        
        return jsonify({
            'ipmi_temperatures': [{'name': t.sensor_name, 'value': t.value} for t in ipmi_temps],
            'gpu_temperatures': [{'name': t.sensor_name, 'value': t.value} for t in gpu_temps]
        })
    except Exception as e:
        logger.error(f"Error in get_temperatures: {e}")
        return jsonify({'error': str(e)}), 500