from producer.clients.fibonacci import FibonacciRpcClient
from fastapi import APIRouter
import pika

router = APIRouter(prefix="/produce", tags=["Producer"])


@router.post("/named")
def send_message_to_named_queue(
    queue: str = "service_A",
    message: str = "Message 1",
):
    """Send message to a named queue on RabbitMQ"""

    parameters = pika.ConnectionParameters(host="broker")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        channel.queue_declare(queue=queue)

        channel.basic_publish(exchange="", routing_key=queue, body=message)

    return {"sent": message}


@router.post("/worker")
def send_message_to_worker_queue(
    queue: str = "service_B",
    message: str = "Task 1",
):
    """Send message to a worker queue on RabbitMQ"""

    parameters = pika.ConnectionParameters(host="broker")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        channel.queue_declare(queue=queue)

        channel.basic_publish(exchange="", routing_key=queue, body=message)

    return {"sent": message}


@router.post("/pubsub")
def send_message_to_subscribers(
    exchange: str = "logs",
    message: str = "Log 1",
):
    """Send message to a fanout exchange on RabbitMQ"""

    parameters = pika.ConnectionParameters(host="broker")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        channel.exchange_declare(exchange=exchange, exchange_type="fanout")

        channel.basic_publish(exchange=exchange, routing_key="", body=message)

    return {"sent": message}


@router.post("/routing")
def send_message_to_specific_subscribers(
    exchange: str = "direct_logs",
    message: str = "Log 1",
    routing_key: str = "critical",
):
    """Send message to a direct exchange on RabbitMQ"""

    parameters = pika.ConnectionParameters(host="broker")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        channel.exchange_declare(exchange=exchange, exchange_type="direct")

        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    return {"sent": message}


@router.post("/topic")
def send_message_to_specific_subscribers(
    exchange: str = "topic_logs",
    message: str = "Log 1",
    routing_key: str = "kern.critical",
):
    """Send message to a topic exchange on RabbitMQ"""

    parameters = pika.ConnectionParameters(host="broker")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        channel.exchange_declare(exchange=exchange, exchange_type="topic")

        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    return {"sent": message}


@router.post("/rpc")
def send_rpc_request(
    value: int = 30,
):
    """Send RPC request on RabbitMQ"""

    fibonacci_rpc = FibonacciRpcClient()
    response = fibonacci_rpc.call(value)

    return {"sent": value, "received": response}
