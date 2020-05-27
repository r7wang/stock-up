## Deployment
Application are normally deployed onto a 3-node cluster for higher availability.

### etcd
Each node requires at least 2 vCPUs, 4GB of memory, and a 10GB boot drive. `etcd` tends to work well with lower latency
and faster disks, hence the application will additionally provision a 1GB SSD.

There is already an [application template](https://console.cloud.google.com/marketplace/details/google/etcd) and set of
[instructions](https://github.com/GoogleCloudPlatform/click-to-deploy/blob/master/k8s/etcd/README.md) on how to use the
template.

#### Chart
There are a few options for working with the application template.
 * deploy the application using the GCP UI
 * generate and copy the full manifest into this repository
 * copy the helm chart into this repository

Deploying through the UI provides the least amount of customization options. Resource names cannot be tailored to the
specific application and tweaks to the architecture or environment variables cannot be made. While this may be
sufficient for prototyping, we will likely want to do some minimal configuration of the production deployment.

Generating the manifest does not allow for customization of the chart, but opens up additional options for providing
values. It also allows us to keep a non-volatile record of the currently deployed application.

Copying the chart facilitates any future modifications to the chart, values, or environment variables. Overall, this is
the most attractive option.

#### Setup
```bash
CLUSTER=etcd-cluster
ZONE=us-east4-c
gcloud container clusters create "${CLUSTER}" \
    --zone="${ZONE}" \
    --cluster-version=1.16.8-gke.15 \
    --machine-type=e2-medium \
    --num-nodes=3 \
    --disk-type=pd-standard \
    --disk-size=10GB \
    --enable-stackdriver-kubernetes
```

#### Teardown
```bash
gcloud container clusters delete "${CLUSTER}" --zone="${ZONE}"
```
