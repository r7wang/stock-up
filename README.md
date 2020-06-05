# stock-up
Polls information about stocks to generate actions.

## Introduction
Running the associated services will produce metrics and visualize them in Grafana.

![Metrics](./doc/images/metrics.png)

## Deployment
Instructions are provided for the following environments.
 * [development](doc/setup/development)
 * [production](doc/setup/production)

## Architecture
Detailed documentation can be found [here](doc/architecture).  

## Next Steps
* Build operational metrics for all services.
    * Usage: CPU, memory, disk, network
    * Counts: message (produced / consumed)
    * Performance: produce + confirmation, analysis
* Figure out how to work with etcd authentication.
* Make applications resilient to broken etcd connection.
* Build out exactly-once semantics for Kafka-based delivery.
* Consider the role of [Redis](https://scalegrid.io/blog/top-redis-use-cases-by-core-data-structure-types/) in
  persisting state of stock analyzer between crashes.
* Consider integrating with [pub/sub](https://cloud.google.com/blog/products/data-analytics/what-to-consider-in-an-apache-kafka-to-pubsub-migration)
  as another message queueing option.
* Add requirements to using this repository.

## Known Issues
* The websocket occasionally closes the connection (for reasons currently unknown), requiring the connection to be
  restarted. Unfortunately, this still takes a few seconds so we lose at least a few seconds worth of data.
* If the stock analyzer service dies, then all state required to maintain the time windows is also lost. A minimum of
  60 seconds (configurable) is required to restore accurate metrics.
* If the stock query service dies, a manual restart is needed and a permanent loss of data is incurred during the
  downtime.
