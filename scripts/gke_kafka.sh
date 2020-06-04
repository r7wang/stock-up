#!/bin/bash

kubectl exec -it stock-kafka-statefulset-0 -- bash -c "\
  kafka-topics.sh --bootstrap-server localhost:9092 --create --topic stock-quotes --partitions 1 --replication-factor 1 && \
  kafka-configs.sh --bootstrap-server localhost:9092 --entity-type topics --entity-name stock-quotes --alter --add-config retention.ms=86400000 && \
  kafka-topics.sh --bootstrap-server localhost:9092 --describe --topics-with-overrides"