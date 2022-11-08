import pika,sys,os

#Broker Queue Parameters 
HOST = 'localhost'
QUEUE = 'REPLY_QUEUE'
ROUTING_KEY = 'REPLY_QUEUE'
EXCHANGE = 'TEST'

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE,durable=True)

    def callback(ch, method, properties, body):
        try:
            data = eval(body)
        except Exception as e:
            data = None
        print(data,'Received data!')
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_consume(queue=QUEUE, on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


        

