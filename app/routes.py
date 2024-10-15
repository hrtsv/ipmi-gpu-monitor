from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from app.models import SensorData
from app.sensors import update_sensor_data
from app.fan_control import adjust_fan_speed
from app import db
from app.auth import login

main = Blueprint('main', __name__)

@main.route('/api/login', methods=['POST'])
def api_login():
    return login()

@main.route('/api/sensor_data', methods=['GET'])
@jwt_required()
def get_sensor_data():
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

@main.route('/api/update_sensors', methods=['POST'])
@jwt_required()
def api_update_sensors():
    update_sensor_data()
    return jsonify({"msg": "Sensor data updated"}), 200

@main.route('/api/adjust_fans', methods=['POST'])
@jwt_required()
def api_adjust_fans():
    fan_speed = adjust_fan_speed(
        current_app.config['IPMI_HOST'],
        current_app.config['IPMI_USERNAME'],
        current_app.config['IPMI_PASSWORD']
    )
    return jsonify({"msg": "Fan speed adjusted", "speed": fan_speed}), 200

@main.route('/api/change_password', methods=['POST'])
@jwt_required()
def api_change_password():
    return change_password()
