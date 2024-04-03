#!/usr/bin/env python
import pika, json
import os, sys, requests

def main():
    credentials = pika.PlainCredentials('admin', 'admin123')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='topology-tsn')

    response = requests.get("http://localhost:8004/tsn-topology")
    if response.status_code == 200:
        tsn_topology = response.json()
        # print("Response data:", tsn_topology)

    channel.basic_publish(exchange='', routing_key='topology-tsn', body=json.dumps(tsn_topology))

    print(" [x] Sent TSN Topology")

    response = requests.get("http://localhost:8004/metro-topology")
    if response.status_code == 200:
        metro_topology = response.json()
        # print("Response data:", metro_topology)

    channel.basic_publish(exchange='', routing_key='topology-metro', body=json.dumps(metro_topology))

    print(" [x] Sent Metro Topology")
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