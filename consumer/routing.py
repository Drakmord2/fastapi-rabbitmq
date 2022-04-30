import pika
import sys
import os


def main(exchange, routing_key):
    parameters = pika.ConnectionParameters(host="localhost")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        channel.exchange_declare(exchange=exchange, exchange_type="direct")
        result = channel.queue_declare(queue="", exclusive=True)
        channel.queue_bind(
            queue=result.method.queue, exchange=exchange, routing_key=routing_key
        )

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=result.method.queue, on_message_callback=callback)

        print("[*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()


if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2])
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
