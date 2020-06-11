#!/bin/bash

docker tag bitnami/etcd:3.4.7 $ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com/etcd:3.4.7
docker push $ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com/etcd:3.4.7

