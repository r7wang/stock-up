#!/bin/bash

REPO="$ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com"

docker tag bitnami/etcd:3.4.7 $REPO/etcd:3.4.7
docker push $REPO/etcd:3.4.7

docker tag bitnami/zookeeper:3.6.1 $REPO/zookeeper:3.6.1
docker push $REPO/zookeeper:3.6.1

