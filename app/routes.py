from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, current_user
from app.models import SensorData
from app import db
from app.sensors import update_sensor_data
from app.auth import login

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/login', methods=['POST'])
def api_login():
    return login()

@main.route('/api/temperatures', methods=['GET'])
def get_temperatures():
    update_sensor_data()  # Update sensor data before fetching
    ipmi_temps = SensorData.query.filter_by(sensor_type='IPMI').order_by(SensorData.timestamp.desc()).limit(10).all()
    gpu_temps = SensorData.query.filter_by(sensor_type='GPU').order_by(SensorData.timestamp.desc()).limit(10).all()
    
    return jsonify({
        'ipmi_temperatures': [{'name': t.sensor_name, 'value': t.value} for t in ipmi_temps],
        'gpu_temperatures': [{'name': t.sensor_name, 'value': t.value} for t in gpu_temps]
    })

# Keep other routes as they were