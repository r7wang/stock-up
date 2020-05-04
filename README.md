# stock-up
Polls information about stocks to generate actions.

## Setup
Turn on service dependencies.

```bash
docker-compose up -d zookeeper kafka influxdb grafana
```

Configure `influxdb`.
```bash
docker exec -it stock-up_influxdb_1 bash
influx
CREATE DATABASE "stock" WITH DURATION 7d NAME "stock_rp"
```

Start consuming from the Kafka topic.

```bash
docker-compose up -d stock-analyzer
```

Start generating stock quotes.

```bash
docker-compose up -d stock-query
```
