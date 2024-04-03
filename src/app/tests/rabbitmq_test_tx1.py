#!/usr/bin/env python
import pika, json
import os, sys

def main ():
    credentials = pika.PlainCredentials('admin', 'admin123')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='metrics')

    channel.basic_publish(exchange='', routing_key='metrics', body='Meeeetrics')

    print(" [x] Sent Metrics")
    connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)