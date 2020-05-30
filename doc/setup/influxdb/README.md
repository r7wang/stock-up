## Setup InfluxDB
The application is configured to use InfluxDB as a time-series database for storing all custom metrics.

Turn on service.
```bash
docker-compose up -d influxdb
```

Create the databases and their retention policies.
```bash
docker exec -it stock-up_influxdb_1 bash
influx
CREATE DATABASE "stock" WITH DURATION 7d NAME "stock_rp"
CREATE DATABASE "kafka" WITH DURATION 7d NAME "kafka_rp"
```
