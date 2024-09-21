import json
import pika
from django.conf import settings
from retry import retry

ROUTING_KEY = 'frontend'  # use name of project
EXCHANGE = 'backend_exchange2'

#   params = pika.URLParameters(settings.RABBITMQ_URL)
params = pika.URLParameters('amqp://guest:guest@rabbitmq:5672/?heartbeat=600')
params._socket_timeout = 5
print(params)

connection = pika.BlockingConnection(params)

channel = connection.channel()
print('Connected')


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def publish(method, body):
    print('Publishing Started')
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange=EXCHANGE, routing_key=ROUTING_KEY, body=json.dumps(body), properties=properties)
