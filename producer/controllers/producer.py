from fastapi import APIRouter, Response
import pika

router = APIRouter(prefix="/produce", tags=["Producer"])


@router.get("/")
def send_message(
    response: Response,
    exchange: str = "amq.direct",
    queue: str = "service_A",
    routing_key: str = "serv.A",
    message: str = "Message 1",
):
    """Send message to RabbitMQ"""

    parameters = pika.ConnectionParameters(host="broker")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        channel.queue_declare(queue=queue, durable=False)
        channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    return {"msg": message}
