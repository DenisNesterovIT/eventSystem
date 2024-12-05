import pika

def callback(ch, method, properties, body):
    message = body.decode()
    user, text = message.split(":", 1)
    screaming_message = f"{user}:{text.upper()}"

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='screaming_to_publish_queue')
    channel.basic_publish(exchange='', routing_key='screaming_to_publish_queue', body=screaming_message)
    connection.close()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='filter_to_screaming_queue')

channel.basic_consume(queue='filter_to_screaming_queue', on_message_callback=callback, auto_ack=True)
print('SCREAMING Service running...')
channel.start_consuming()
