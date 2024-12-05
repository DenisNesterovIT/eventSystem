import pika

STOP_WORDS = ["bird-watching", "ailurophobia", "mango"]

def callback(ch, method, properties, body):
    message = body.decode()
    user, text = message.split(":", 1)

    if any(word in text for word in STOP_WORDS):
        print(f"Filtered out message: {text}")
    else:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='filter_to_screaming_queue')
        channel.basic_publish(exchange='', routing_key='filter_to_screaming_queue', body=message)
        connection.close()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='api_to_filter_queue')

channel.basic_consume(queue='api_to_filter_queue', on_message_callback=callback, auto_ack=True)
print('Filter Service running...')
channel.start_consuming()
