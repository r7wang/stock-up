## Development
Setup one of the following message queues.
 * [Kafka](kafka)
 * [RabbitMQ](rabbitmq)

Setup [influxdb](influxdb).

Setup [grafana](grafana).

Start consuming stock quotes.
```bash
docker-compose up -d stock-analyzer
```

Start generating stock quotes.
```bash
docker-compose up -d stock-query
```

Use dynamic configuration to define desired behavior.
 * [stock-query](/stock_query)
 * [stock-analyzer](/stock_analyzer)
