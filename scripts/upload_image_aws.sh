#!/bin/bash

REPO="$ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com"

IMAGE=stock-query:0.1
docker tag $IMAGE $REPO/$IMAGE
docker push $REPO/$IMAGE

IMAGE=stock-analyzer:0.1
docker tag $IMAGE $REPO/$IMAGE
docker push $REPO/$IMAGE

IMAGE=etcd:3.4.7
docker tag bitnami/$IMAGE $REPO/$IMAGE
docker push $REPO/$IMAGE

IMAGE=zookeeper:3.6.1
docker tag bitnami/$IMAGE $REPO/$IMAGE
docker push $REPO/$IMAGE

IMAGE=kafka:2.5.0
docker tag bitnami/$IMAGE $REPO/$IMAGE
docker push $REPO/$IMAGE

IMAGE=influxdb:1.8.0
docker tag bitnami/$IMAGE $REPO/$IMAGE
docker push $REPO/$IMAGE

IMAGE=grafana:6.7.3
docker tag bitnami/$IMAGE $REPO/$IMAGE
docker push $REPO/$IMAGE

