from flask import Blueprint, jsonify, render_template
from app.models import SensorData
from app import db
from app.sensors import update_sensor_data
import logging

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/sensor_data')
def get_sensor_data():
    try:
        update_sensor_data()
        temperatures = SensorData.query.filter_by(sensor_type='Temperature').order_by(SensorData.timestamp.desc()).limit(10).all()
        fans = SensorData.query.filter_by(sensor_type='Fan').order_by(SensorData.timestamp.desc()).limit(10).all()
        
        temp_data = {}
        fan_data = {}
        
        for temp in temperatures:
            if temp.sensor_name not in temp_data:
                temp_data[temp.sensor_name] = []
            temp_data[temp.sensor_name].append({
                'timestamp': temp.timestamp.isoformat(),
                'value': temp.value
            })
        
        for fan in fans:
            if fan.sensor_name not in fan_data:
                fan_data[fan.sensor_name] = []
            fan_data[fan.sensor_name].append({
                'timestamp': fan.timestamp.isoformat(),
                'value': fan.value
            })
        
        return jsonify({
            'temperatures': temp_data,
            'fans': fan_data
        })
    except Exception as e:
        logger.error(f"Error in get_sensor_data: {e}")
        return jsonify({'error': str(e)}), 500