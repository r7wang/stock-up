## kafka-jmx

This is an image that packages `bitnami/kafka` with the `jolokia` JVM agent to expose HTTP metrics on port `9992`.

### Building
Run the following commands from this directory.

```bash
docker build -t kafka-jmx:0.1 .
```

### Usage
With the container running, you can query Kafka metrics directly from the browser. See the examples below.

```bash
# Search available metrics
http://localhost:9992/jolokia/search/*:*

# Query metric by type and name
http://localhost:9992/jolokia/read/kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
```

### Articles
[Jolokia Protocol Reference](https://jolokia.org/reference/html/protocol.html)  
[Monitoring Kafka with Jolokia](https://pushed.to/cokeSchlumpf/rethink-it/posts/misc/monitoring-kafka.md)  
