from flask import Blueprint, jsonify, request, render_template
from app.models import SensorData
from app import db
from app.sensors import update_sensor_data
from sqlalchemy import func
import logging
from datetime import datetime, timedelta

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/sensor_data')
def get_sensor_data():
    try:
        update_sensor_data()  # Update sensor data before fetching
        
        # Get data for the last 24 hours
        start_time = datetime.utcnow() - timedelta(hours=24)
        
        temp_data = SensorData.query.filter(
            SensorData.sensor_type == 'Temperature',
            SensorData.timestamp >= start_time
        ).order_by(SensorData.timestamp.asc()).all()
        
        fan_data = SensorData.query.filter(
            SensorData.sensor_type == 'Fan',
            SensorData.timestamp >= start_time
        ).order_by(SensorData.timestamp.asc()).all()
        
        # Group data by sensor name
        temp_grouped = {}
        fan_grouped = {}
        
        for data in temp_data:
            if data.sensor_name not in temp_grouped:
                temp_grouped[data.sensor_name] = []
            temp_grouped[data.sensor_name].append({
                'timestamp': data.timestamp.isoformat(),
                'value': data.value
            })
        
        for data in fan_data:
            if data.sensor_name not in fan_grouped:
                fan_grouped[data.sensor_name] = []
            fan_grouped[data.sensor_name].append({
                'timestamp': data.timestamp.isoformat(),
                'value': data.value
            })
        
        return jsonify({
            'temperatures': temp_grouped,
            'fans': fan_grouped
        })
    except Exception as e:
        logger.error(f"Error in get_sensor_data: {e}")
        return jsonify({'error': str(e)}), 500