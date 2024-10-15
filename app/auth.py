from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, current_user
from app.models import User
from app import jwt, db

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)

@jwt_required()
def change_password():
    current_password = request.json.get("current_password", None)
    new_password = request.json.get("new_password", None)

    if not current_user.check_password(current_password):
        return jsonify({"msg": "Current password is incorrect"}), 401

    current_user.set_password(new_password)
    db.session.commit()

    return jsonify({"msg": "Password successfully changed"}), 200