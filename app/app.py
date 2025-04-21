from flask import Flask, request
import logging
import os

app = Flask(__name__)

# Ensure logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
)

@app.before_request
def log_request_info():
    logging.info(f"{request.method} request to {request.path} from {request.remote_addr}")

@app.route('/')
def home():
    return "Hello from your Dockerized Flask app! (created by Mohammad Alghzawi)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

