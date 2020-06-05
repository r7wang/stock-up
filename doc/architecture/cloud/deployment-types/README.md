## Deployment Types

### Google Compute Engine: Containers in Unmanaged VMs
This involves manually allocating VM instances and specifying an individual image to be run on each instance. Deploying
a container is documented [here](https://cloud.google.com/compute/docs/containers/deploying-containers). Setting
environment variables can be done by modifying `/etc/profile` on the instance, then restarting it.

#### Advantages
 * The workflow for provisioning containers on VM instances is clearly defined.
 * Internal IPs and DNS (using the instance name) are automatically configured for service-to-service communication
   within the same network.
 * Exposing an instance to the internet through an external IP and firewall policies is very straightforward. 

#### Disadvantages
 * Unless manually instrumenting container operations, every container must be run on a separate instance. This can
   lead to waste of server resources because the instance has to be provisioned against peak load.
 * Setting up a cluster of services requires careful _manual_ configuration.
 * It can be difficult to ensure correctness of the currently provisioned devices without using declarative tools.
 * Workflow relies on startup scripts to configure an instance correctly. This adds additional complexity because
   containerized deployment has multiple startup phases, one for the instance and one for the container.
 * Setting up TLS termination using an HTTPS load balancer is non-trivial; requires building multiple GCP resources.
 * Stackdriver logging is very noisy, making it difficult to find relevant logs.

#### Notes
 * Container images must be versioned incrementally to ensure that VMs automatically pick up the latest images. 
 * There are easier ways of setting up web applications and the hosting environment around those applications. Both
   `App Engine` and `Cloud Run` provide higher level abstractions.

#### Assessment
This option allows us to get services up and running with less effort in exchange for sacrificing high-availability and
scale, which is very attractive for building out a minimum viable product.

#### References
GCP has relevant documentation on some of the concepts below.
 * [Load balancing](https://cloud.google.com/load-balancing/docs/how-to)

Bitnami has provided options for single VM deployments without the use of containers.
 * [etcd](https://console.cloud.google.com/marketplace/details/bitnami-launchpad/etcd)
 * [kafka](https://console.cloud.google.com/marketplace/details/bitnami-launchpad/kafka)

### Google Kubernetes Engine: Single Cluster with Node Pools
This involves creating a cluster and assigning applications to run on specific node pools. Applications are able to
communicate with each other directly at either the `Pod` or the `Service` level, through DNS-based [service discovery](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/).
`Pod` communication tends to be used when dealing with cluster configuration for a distributed application, potentially
requiring a headless `Service` to [establish network identity](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/),
if using `StatefulSet`. `Service` communication is more frequently used for round-robin load balancing of stateless
applications within the cluster.

#### Advantages
 * Compared to unmanaged VMs, there is not much additional work to provision a cluster and its applications using an
   automated approach.
 * Internal IPs and DNS (using the instance name) are automatically configured for service-to-service communication
   within the same network.
 * Cluster resources can be efficiently allocated to maximize resource usage.
 * Cluster resources can be easily and independently scaled, without affecting underlying applications.
 * Kubernetes applies an additional layer of abstraction around the concept of `Ingress`, meaning that load balancing
   resources don't have to be explicitly managed.
 * Application logs are isolated from node logging.
 * Cluster management pricing is a fixed cost per cluster.
 * Kubernetes provides effective approaches to defining liveness checks and health checks.

#### Disadvantages
 * Developers must understand some of the intricacies behind updating resources because they don't always update
   correctly and are sometimes dependent on order of creation.
 * Kubernetes is a non-trivial technology that requires an in-depth understanding of its concepts.

#### Notes
 * Using a single cluster avoids having to configure an internal load balancer to expose services from other clusters
   within the same VPC.
 * It also has the advantage of reducing the cluster management fee, given that it's a fixed cost per
   cluster.
 * There may be disadvantages in terms of cluster isolation, but this requires further investigation.

#### Assessment
This option currently seems to be the most viable for a long-term solution involving multiple services at scale. The
complexity of Kubernetes may not be warranted below a certain scale.

### Google Kubernetes Engine: Multiple Clusters
This involves creating a cluster for each application, which shares a lot of similarities with using a single cluster.
While there is more work to set up cluster-to-cluster networking, there is no need to manage multiple node pools and
which applications can be deployed across those node pools. 

### Fully Managed
This is not applicable to all applications and is likely to vary in terms of feature set and pricing.

For reference, Confluent offers fully-managed solutions for [Kafka](https://console.cloud.google.com/marketplace/product/endpoints/payg-prod.gcpmarketplace.confluent.cloud).
Their implementation is agnostic to cloud platform but there is likely significant cost in migration and re-integrating
with different cloud platforms so there may not be much advantage in terms of avoiding vendor lock-in.
