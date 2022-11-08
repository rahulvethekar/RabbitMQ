import pika

def generate_queue(**kwargs):
    connection  = pika.BlockingConnection(pika.ConnectionParameters(kwargs['host']))
    channel     = connection.channel()
    channel.queue_declare(queue=kwargs['queue'],durable=True)
    channel.basic_publish(exchange='',routing_key=kwargs['routing_key'],body=str(kwargs['data']),
                properties=pika.BasicProperties(delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE)) 
                
    print(" [x] Sent %r" % kwargs['data'])
    connection.close() 