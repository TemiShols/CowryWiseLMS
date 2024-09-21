import json
import pika, threading
from .models import Book

ROUTING_KEY = 'backend'
EXCHANGE = 'backend_exchange2'
THREADS = 5


class FrontendListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@rabbitmq:5672/?heartbeat=600'))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(queue=queue_name, exchange=EXCHANGE, routing_key=ROUTING_KEY)
        self.channel.basic_qos(prefetch_count=THREADS * 10)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback)

    def callback(self, channel, method, properties, body):
        print('Received in Frontend')
        data = json.loads(body)

        if properties.content_type == 'book created':
            book = Book.objects.create(id=data['id'], title=data['title'],
                                       author=data['author'], publisher=data['publisher'],
                                       category=data['category'], is_available=data['is_available'],
                                       available_date=data['available_date'])
            book.save()
            print('book created')

        elif properties.content_type == 'book updated':
            book = Book.objects.get(pk=data['id'])
            #   book(**data).save()
            book.id = data['id'], book.user = data['user'],
            book.book = data['book'], borrow_date = data['borrow_date'],
            book.return_date = data['return_date']
            book.save()
            print('book updated')

        elif properties.content_type == 'book deleted':
            book = Book.objects.get(pk=data['id'])
            book.delete()
            print('book Deleted')
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print('Consuming Started')
        self.channel.start_consuming()
