## Extension Image

This is an image that packages `bitnami/zookeeper` with a built-in liveness and readiness probe that can be used for
Kubernetes deployments. With the default image, we can only do TCP checks, which end up spamming the logs with cryptic
warning messages.

### Building
Run the following commands from this directory.

```bash
docker build -t gcr.io/cosmic-heaven-255312/zookeeper-ext:3.6.1 .
```

### Usage
Liveness and readiness can be built using `netcat`. See [this](https://unofficial-kubernetes.readthedocs.io/en/latest/tutorials/stateful-application/zookeeper/)
guide for details.

### References
Bitnami provides a sample helm chart [here](https://github.com/bitnami/charts/blob/master/bitnami/zookeeper/templates/statefulset.yaml).
