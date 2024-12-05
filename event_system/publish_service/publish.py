import pika
import smtplib
from email.mime.text import MIMEText

EMAIL_ADDRESS = "ol27281480@gmail.com"
EMAIL_PASSWORD = "nwjd hffl mvud cwhb"
RECIPIENT_EMAIL = "denesterov3005@yandex.ru"

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

def callback(ch, method, properties, body):
    message = body.decode()
    user, text = message.split(":", 1)
    send_email(user, text)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='screaming_to_publish_queue')

channel.basic_consume(queue='screaming_to_publish_queue', on_message_callback=callback, auto_ack=True)
print('Publish Service running...')
channel.start_consuming()
