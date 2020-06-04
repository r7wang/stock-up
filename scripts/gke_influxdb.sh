#!/bin/bash

kubectl exec -it stock-influxdb-statefulset-0 -- bash -c "\
  influx -username admin -password '$INFLUXDB_PASSWORD' -execute 'CREATE DATABASE stock WITH DURATION 7d NAME stock_rp' && \
  influx -username admin -password '$INFLUXDB_PASSWORD' -execute 'SHOW DATABASES'"