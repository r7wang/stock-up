# stock-up
Polls information about stocks to generate actions.

## Setup
Turn on service dependencies.

```bash
docker-compose up -d zookeeper kafka influxdb grafana
```

Configure `kafka`.
```bash
docker exec -it stock-up_kafka_1 bash
kafka-configs.sh --bootstrap-server kafka:9092 --entity-type topics --entity-name stock-quotes --alter --add-config retention.ms=86400000

# The line below should output something like this:
#
# Topic: stock-quotes
#     PartitionCount: 1
#     ReplicationFactor: 1
#     Configs: segment.bytes=1073741824,retention.ms=86400000
kafka-topics.sh --bootstrap-server kafka:9092 --describe --topics-with-overrides
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
