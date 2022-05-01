# FastAPI as a RabbitMQ producer/consumer

## Setup

You'll need [Docker](https://docs.docker.com/engine/install/) and [Docker-Compose](https://docs.docker.com/compose/install/) to run the application. With both dependencies installed, just run on a terminal:

```bash
docker-compose up
```

This will setup a ready to use [FastAPI](https://fastapi.tiangolo.com/) and [RabbitMQ](https://www.rabbitmq.com) servers on ports `5000` and `5672`, respectively.

---

## Web Interfaces

The Producers are executed through REST endpoints and can be run on the Swagger UI configured at the URL below:

`http://localhost:5000/docs`

Exchanges, Queues, Consumers and more can be inspected through the RabbitMQ management console at:

`http://localhost:8080`

---

## Consumers

The Consumers (or Workers) are executed on separate terminals. Make sure you create a virtual environment with all the required dependencies by running:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Below are the pre-defined consumers available for use:

1. Consume a named queue

```bash
python consumer/named_queue.py "queue_name"
```

2. Concurrently consume tasks from a queue

```bash
python consumer/worker_queue.py "queue_name"
```

3. Consume a queue in parallel using the Publisher/Subscriber pattern

```bash
python -u consumer/pubsub.py "exchange_name"
```

4. Consume routed messages

```bash
python consumer/routing.py "exchange_name" "routing_key1" "routing_key2" ...
```

5. Consume messages from specific Topics

```bash
python consumer/topic.py "exchange_name" "routing_key1" "routing_key2" ...
```

6. Reply to RPC calls

```bash
python consumer/rpc.py
```
