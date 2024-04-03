#!/usr/bin/env python
import pika, sys, os

def main():
    credentials = pika.PlainCredentials('admin', 'admin123')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    print('connected')

    channel.queue_declare(queue='hello')
    channel.queue_declare(queue='topology-tsn')
    channel.queue_declare(queue='topology-metro')
    channel.queue_declare(queue='metrics')

    def callback(ch, method, properties, body):
        if method.routing_key == 'topology-tsn':
            print(f" [x] Received TSN topology data with {len(body)} characteres")
        elif method.routing_key == 'topology-metro':
            print(f" [x] Received Metro topology data with {len(body)} characteres")
        elif method.routing_key == 'metrics':
            print(f" [x] Received metrics data: {body.decode()}")
        elif method.routing_key == 'hello': 
            print(f" [x] Received hello message")
        else:
            print(f" [x] Unknown message")
        # print(f" [x] Received data {properties}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='topology-tsn', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='topology-metro', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='metrics', on_message_callback=callback, auto_ack=True)

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
