from connect import client
from models import Contact

from pickle import dumps

from faker import Faker
import pika


def insert_data():
    fake = Faker()

    contacts = [Contact(fullname=fake.name(), email=fake.email()) for num in range(15)]
    contacts_id = Contact.objects().insert(contacts, load_bulk=False)

    return contacts_id


def send_messages(contacts_id):
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='task_mock', exchange_type='direct')
    channel.queue_declare(queue='task_queue', durable=True)
    channel.queue_bind(exchange='task_mock', queue='task_queue')

    for object_id in contacts_id:
        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=dumps(object_id),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
            )
    connection.close()


if __name__ == "__main__":
    contacts_id = insert_data()
    send_messages(contacts_id)