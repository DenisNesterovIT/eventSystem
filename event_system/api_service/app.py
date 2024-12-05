from flask import Flask, request, jsonify
import pika
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app)

def publish_message_to_queue(queue_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    connection.close()

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    app.logger.info(f"Received data: {data}")
    data = request.get_json()
    user = data.get('user')
    message = data.get('message')

    if not user or not message:
        return jsonify({'error': 'Invalid data'}), 400

    message_data = f"{user}:{message}"
    publish_message_to_queue('api_to_filter_queue', message_data)
    return jsonify({'status': 'Message sent to filter'}), 200

if __name__ == '__main__':
    app.run(port=5050)
