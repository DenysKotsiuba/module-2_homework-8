from connect import client
from models import Contact

from pickle import loads
from sys import exit

import pika


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


def callback(ch, method, properties, body):
    message = loads(body)
    print(message)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    send_to_email(message)




channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)


def send_to_email(contacts_id):
    contact = Contact.objects(id=contacts_id)
    contact.update(send_status=True)


if __name__ == "__main__":
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        exit(0)