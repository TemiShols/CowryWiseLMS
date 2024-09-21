import json
import pika, threading
from .models import Book, NewUser

ROUTING_KEY = 'frontend'
EXCHANGE = 'backend_exchange2'
THREADS = 5


class BackendConsumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@rabbitmq:5672/?heartbeat=600'))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')
        # self.channel.queue_declare(queue=QUEUE_NAME, auto_delete=False)
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(queue=queue_name, exchange=EXCHANGE, routing_key=ROUTING_KEY)
        self.channel.basic_qos(prefetch_count=THREADS * 10)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)

    def callback(self, channel, method, properties, body):
        print('Received in Backend')
        data = json.loads(body)

        if properties.content_type == 'book borrowed':
            borrowed_book = Book.objects.create(id=data['id'], user=data['user'],
                                                        book=data['book'], borrow_date=data['borrow_date'],
                                                        return_date=data['return_date'])
            borrowed_book.save()
            print('book borrowed')
        elif properties.content_type == 'new user created':
            user = NewUser.objects.create(username=data['username'], email=data['email'])
            user.set_password(data['password'])
            user.save()
            print('new user created')
        elif properties.content_type == 'book deleted':
            borrowed_book = Book.objects.get(pk=data['id'])
            borrowed_book.delete()
            print('book Deleted')
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print('Consuming Started')
        self.channel.start_consuming()
