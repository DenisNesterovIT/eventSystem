import multiprocessing
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

STOP_WORDS = ["bird-watching", "ailurophobia", "mango"]
EMAIL_ADDRESS = "ol27281480@gmail.com"
EMAIL_PASSWORD = "nwjd hffl mvud cwhb"
RECIPIENT_EMAIL = "denisnesterov3005@yandex.ru"

# REST API Service
def rest_api_service(output_queue):
    app = Flask(__name__)

    @app.route('/send', methods=['POST'])
    def send_message():
        data = request.get_json()
        user = data.get('user')
        message = data.get('message')

        if not user or not message:
            return jsonify({'error': 'Invalid data'}), 400

        message_data = f"{user}:{message}"
        output_queue.put(message_data)
        return jsonify({'status': 'Message sent to filter'}), 200

    app.run(port=5050)

# Filter Service
def filter_service(input_queue, output_queue):
    while True:
        message = input_queue.get()  # Blocking until a message is available
        user, text = message.split(":", 1)

        if any(word in text for word in STOP_WORDS):
            print(f"Filtered out message: {text}")
        else:
            output_queue.put(message)

# SCREAMING Service
def screaming_service(input_queue, output_queue):
    while True:
        message = input_queue.get()
        user, text = message.split(":", 1)
        screaming_message = f"{user}:{text.upper()}"
        output_queue.put(screaming_message)

# Publish Service
def publish_service(input_queue):
    def send_email(user, message):
        subject = f"Message from {user}"
        body = f"From user: {user}\nMessage: {message}"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

    while True:
        message = input_queue.get()
        user, text = message.split(":", 1)
        send_email(user, text)
        print(f"Email sent: From {user}, Message: {text}")

# Main Function to Initialize and Connect Services
if __name__ == '__main__':
    # Define communication queues
    api_to_filter_queue = multiprocessing.Queue()
    filter_to_screaming_queue = multiprocessing.Queue()
    screaming_to_publish_queue = multiprocessing.Queue()

    # Create and start processes for each service
    api_process = multiprocessing.Process(target=rest_api_service, args=(api_to_filter_queue,))
    filter_process = multiprocessing.Process(target=filter_service, args=(api_to_filter_queue, filter_to_screaming_queue))
    screaming_process = multiprocessing.Process(target=screaming_service, args=(filter_to_screaming_queue, screaming_to_publish_queue))
    publish_process = multiprocessing.Process(target=publish_service, args=(screaming_to_publish_queue,))

    # Start all processes
    api_process.start()
    filter_process.start()
    screaming_process.start()
    publish_process.start()

    # Wait for processes to finish (blocking call)
    api_process.join()
    filter_process.join()
    screaming_process.join()
    publish_process.join()
