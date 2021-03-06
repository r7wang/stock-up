## Setup Kafka
The application is configured to run against a configurable message queue stack. Follow these instructions to configure
Kafka.

Set the `MESSAGE_QUEUE_TYPE` environment variable for `stock-analyzer` and `stock-query` to `kafka`.

Zookeeper is a Kafka dependency and needs to be available.
```bash
docker-compose up -d zookeeper
```

Turn on service.
```bash
docker-compose up -d kafka
```

Create the topic and set its retention policy.
```bash
docker exec -it stock-up_kafka_1 bash
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic stock-quotes --partitions 1 --replication-factor 1
kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name stock-quotes --alter --add-config retention.ms=86400000

# The line below should output something like this:
#
# Topic: stock-quotes
#     PartitionCount: 1
#     ReplicationFactor: 1
#     Configs: segment.bytes=1073741824,retention.ms=86400000
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topics-with-overrides
```

See architecture [notes](/doc/architecture/kafka) for more information.
