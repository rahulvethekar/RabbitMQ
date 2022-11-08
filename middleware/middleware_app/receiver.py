import pika
import os
import sys
import requests
import time
from sys import path
from django import setup
from os import environ

from pprint import pprint
pprint(sys.path)

path.append('/home/neosoft/Backup/Rabbit_MQ/homelane_assignment/middleware')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'middleware.settings')
setup()

#Broker Queue parameters
HOST = 'localhost'
QUEUE = 'queue1'
ROUTING_KEY = 'queue1'

from middleware_app.models import MaxCount

#Base url
BASE_URL = 'http://127.0.0.1:8002'

#Max Count
def max_count(kwargs):
    try:
        max_limit = MaxCount.objects.get(**kwargs).count    
    except Exception as e:
        print(e,'MAX EXCEPTION')
        # max_limit = None
    return max_limit

def create_broker_queue(**kwargs):
    connection  = pika.BlockingConnection(pika.ConnectionParameters(kwargs['HOST']))
    channel     = connection.channel()
    channel.queue_declare(queue=kwargs['QUEUE'],durable=True)
    channel.basic_publish(exchange='',routing_key=kwargs['ROUTING_KEY'],body=str(kwargs['data']),
    properties=pika.BasicProperties(delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE))
    connection.close()

def get_response(data,channel):
    temp_data = data
    url = data.get('url')
    method = data.get('method')
    #print("method:",method)
    #print(data)
    # print(url)
    endpoint = f"{BASE_URL}/{url}"
    # print(endpoint)
    
    try:
        #if application start working back
        
        if method == 'get':
            response = requests.get(endpoint) 

        elif method == 'post':
            d1 = {}
            for i in data:
                if i != 'url' and i != 'method':
                    d1[i] = data.get(i)
                    #print(d1)
            response = requests.post(endpoint,d1)

        elif method == 'put':
            d1 = {}
            for i in data:
                if i != 'url' and i != 'method':
                    d1[i] = data.get(i)
            response = requests.put(endpoint,data=d1)

        elif method == 'delete':
            d1 = {}
            for i in data:
                if i != 'url' and i != 'method':
                    d1[i] = data.get(i)
                    #print(d1)
            response = requests.delete(endpoint,data=d1)
            #print(response)
        #sent to reply queue
        create_broker_queue(
                HOST = "localhost",
                QUEUE = 'REPLY_QUEUE',
                ROUTING_KEY = "REPLY_QUEUE",
                data = response.json()
        )

    except Exception as e: 
        # counter = 0
        # counter +=1
        # # print(counter)
   
        max_retry_limit = max_count({'url':temp_data['url']})
        
        count = int(temp_data['retry_count']) + 1
        temp_data.update({
            'retry_count': count
        })
        print("Trying again....",count)
        #print(e)


        time.sleep(6)
        # Max limit exceed.
        if  count < max_retry_limit :
            channel.basic_publish(exchange='',routing_key=ROUTING_KEY,body=str(temp_data))                  
        else:
            #Sent to reply queue
            print("Exceed max limit...")
            create_broker_queue(
                HOST = "localhost",
                QUEUE = "REPLY_QUEUE",
                ROUTING_KEY = "REPLY_QUEUE",
                data = temp_data
            )


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE,durable=True)

    def callback(ch, method, properties, body):
        
        try:
            data = eval(body)            
        except Exception as e:            
            data = None    

        ch.basic_ack(delivery_tag = method.delivery_tag)
        
        if data:
            get_response(data,channel)      
        

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



