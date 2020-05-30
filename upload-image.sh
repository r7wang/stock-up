#!/bin/bash

docker tag stock-query:0.1 gcr.io/$PROJECT_ID/stock-query:0.1
docker push gcr.io/$PROJECT_ID/stock-query:0.1

docker tag stock-analyzer:0.1 gcr.io/$PROJECT_ID/stock-analyzer:0.1
docker push gcr.io/$PROJECT_ID/stock-analyzer:0.1

