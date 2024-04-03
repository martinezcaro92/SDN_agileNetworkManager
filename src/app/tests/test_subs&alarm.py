import pytest
import pika
from time import sleep

rabbitmq_user = "admin"
rabbitmq_pass = "admin123"
rabbitmq_host = "rabbitmq" 

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)

def test_rabbitmq_is_available():

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials))
        connection.close()
        rabbitmq_available = True
    except pika.exceptions.ConnectionClosed as e:
        rabbitmq_available = False

    assert rabbitmq_available == True, f"RabbitMQ no está disponible en {rabbitmq_host}"


def test_queue_metrics():

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue="metrics", passive=True)
        queues_exist = True
        connection.close()

    except pika.exceptions.ConnectionClosed as e:
        queues_exist = False

    assert queues_exist == True, "The 'metrics' queue is not active"

def test_send_and_receive_message_metrics():
    message = "Hola, RabbitMQ! via metrics queue"

    response = send_and_receive_message("metrics", message)

    assert response == message, "The sent and received message does not match"

def test_queue_topology_tsn():

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue="topology-tsn", passive=True)
        queues_exist = True
        connection.close()

    except pika.exceptions.ConnectionClosed as e:
        queues_exist = False

    assert queues_exist == True, "The 'topology-tsn' queue is not active"

def test_send_and_receive_message_topology_tsn():
    message = "Hola, RabbitMQ! via topology-tsn queue"

    response = send_and_receive_message("topology-tsn", message)

    assert response == message, "The sent and received message does not match"

def test_queue_topology_metro():

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue="topology-metro", passive=True)
        queues_exist = True
        connection.close()

    except pika.exceptions.ConnectionClosed as e:
        queues_exist = False

    assert queues_exist == True, "The 'topology-metro' queue is not active"

def test_send_and_receive_message_topology_metro():
    message = "Hola, RabbitMQ! via topology-tsn queue"

    response = send_and_receive_message("topology-metro", message)

    assert response == message, "The sent and received message does not match"
    


def send_and_receive_message(queue, message):

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
        )
        channel = connection.channel()

        channel.queue_declare(queue=queue)

        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=message
        )
        sleep(0.3)
        method_frame, header_frame, body = channel.basic_get(queue=queue, auto_ack=True)
        connection.close()
        # channel.queue_delete(queue=queue)

        return body.decode("utf-8") if body else None
    except Exception as e:
        raise e








if __name__ == "__main__":
    pytest.main([__file__])
