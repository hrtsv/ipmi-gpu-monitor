from app import create_app
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    logger.info("Starting application")
    app.run(host='0.0.0.0', port=5000)