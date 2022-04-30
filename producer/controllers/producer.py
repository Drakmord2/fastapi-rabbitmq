from fastapi import APIRouter
import pika

router = APIRouter(prefix="/produce", tags=["Producer"])


@router.post("/named")
def send_message_to_named_queue(
    exchange: str = "amq.direct",
    queue: str = "service_A",
    routing_key: str = "serv.A",
    message: str = "Message 1",
):
    """Send message to a named queue on RabbitMQ"""

    parameters = pika.ConnectionParameters(host="broker")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        channel.queue_declare(queue=queue)
        channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    return {"sent": message}


@router.post("/worker")
def send_message_to_worker_queue(
    exchange: str = "amq.direct",
    queue: str = "service_B",
    routing_key: str = "serv.B",
    message: str = "Task 1",
):
    """Send message to a worker queue on RabbitMQ"""

    parameters = pika.ConnectionParameters(host="broker")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        channel.queue_declare(queue=queue)
        channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    return {"sent": message}


@router.post("/pubsub")
def send_message_to_subscribers(
    exchange: str = "logs",
    message: str = "Task 1",
):
    """Send message to a fanout exchange on RabbitMQ"""

    parameters = pika.ConnectionParameters(host="broker")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        channel.exchange_declare(exchange=exchange, exchange_type="fanout")

        channel.basic_publish(exchange=exchange, routing_key="", body=message)

    return {"sent": message}
