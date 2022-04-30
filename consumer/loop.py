import pika
import sys
import os


def main(queue):
    parameters = pika.ConnectionParameters(host="localhost")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=False)

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            reply_queue = queue + "_reply"
            reply_key = method.routing_key

            ch.queue_declare(queue=reply_queue, durable=False)
            ch.queue_bind(
                queue=reply_queue,
                exchange=method.exchange,
                routing_key=reply_key,
            )
            ch.basic_publish(exchange=method.exchange, routing_key=reply_key, body=body)
            print(" [x] Sent %r" % body)

        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        print("[*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
