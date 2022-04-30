import pika
import sys
import os


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def main():
    parameters = pika.ConnectionParameters(host="localhost")

    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()

        channel.queue_declare(queue="rpc_queue")

        def callback(ch, method, props, body):
            n = int(body)

            print(" [x] fib(%s)" % n)
            response = fib(n)

            ch.basic_publish(
                exchange="",
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id=props.correlation_id),
                body=str(response),
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)

            print(
                f"   [.] {props.correlation_id} - {props.reply_to}: {response}",
            )

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue="rpc_queue", on_message_callback=callback)

        print("[*] Awaiting RPC requests To exit press CTRL+C")
        channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
