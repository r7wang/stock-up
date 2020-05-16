## Design Considerations

### Avoiding Message Duplication
Avoiding duplication is very important for data quality because duplication can result in volume and weighted averages
being calculated incorrectly. Kafka supports deduplication using an `enable.idempotence` configuration in conjunction
with other settings, described [here](https://www.cloudkarafka.com/blog/2019-04-10-apache-kafka-idempotent-producer-avoiding-message-duplication.html).
This results in very simple application development.

### Scaling Throughput
Scaling is typically done by increasing partitions, and consequently, brokers. The difficulty here is that after
scaling, it's conceptually difficult to scale down because of the increase in partitions. There must likely be a
process to drain a partition, delete the partition, and restart brokers. This is much more complicated than setting a
configuration to reduce the consumer count. 
