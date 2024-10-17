from flask import Blueprint, jsonify, request, render_template, current_app
import os
import logging

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/')
def index():
    logger.debug(f"Current working directory: {os.getcwd()}")
    logger.debug(f"Contents of current directory: {os.listdir('.')}")
    logger.debug(f"Contents of app directory: {os.listdir('app')}")
    logger.debug(f"Contents of templates directory: {os.listdir('app/templates')}")
    logger.debug(f"Template folder: {current_app.template_folder}")
    return render_template('index.html')

# ... (rest of the routes file)