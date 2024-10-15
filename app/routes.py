from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from app.models import SensorData
from app.sensors import update_sensor_data
from app import db
from app.auth import login
import logging

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/api/sensor_data', methods=['GET'])
@jwt_required()
def get_sensor_data():
    try:
        sensor_type = request.args.get('type')
        limit = request.args.get('limit', 100, type=int)
        
        query = SensorData.query.order_by(SensorData.timestamp.desc())
        if sensor_type:
            query = query.filter_by(sensor_type=sensor_type)
        
        data = query.limit(limit).all()
        return jsonify([{
            'timestamp': d.timestamp,
            'sensor_type': d.sensor_type,
            'sensor_name': d.sensor_name,
            'value': d.value
        } for d in data])
    except Exception as e:
        logger.error(f"Error fetching sensor data: {e}")
        return jsonify({"error": "An error occurred while fetching sensor data"}), 500

@main.route('/api/update_sensors', methods=['POST'])
@jwt_required()
def api_update_sensors():
    try:
        update_sensor_data()
        return jsonify({"msg": "Sensor data updated"}), 200
    except Exception as e:
        logger.error(f"Error updating sensor data: {e}")
        return jsonify({"error": "An error occurred while updating sensor data"}), 500

# ... rest of the routes remain the same