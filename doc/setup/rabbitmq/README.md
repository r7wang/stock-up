## Setup RabbitMQ
The application is configured to run against a configurable message queue stack. Follow these instructions to configure
RabbitMQ.

Add this section to `docker-compose.yaml`.
```bash
  rabbitmq:
    image: bitnami/rabbitmq:3.8.3
    networks:
      - stock-network
    volumes:
      - '.rabbitmq_data:/bitnami'
    environment:
      - RABBITMQ_USERNAME=rmq
      - RABBITMQ_PASSWORD=rmq-password
      - RABBITMQ_VHOST=stocks
```

Set the `MESSAGE_QUEUE_TYPE` environment variable for `stock-analyzer` and `stock-query` to `rmq`.

Turn on service.
```bash
docker-compose up -d rabbitmq
```

Configure default credentials.
```bash
docker exec -it stock-up_rabbitmq_1 bash
rabbitmqctl add_user stock-query rmq-password
rabbitmqctl set_permissions -p stocks stock-query ".*" ".*" ".*"
``` 

See architecture [notes](/doc/architecture/rabbitmq) for more information.
