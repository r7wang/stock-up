## Deployment Types

#### Google Compute Engine: Containers in VM
This involves manually allocating VMs and specifying an individual image to be run on each VM. Deploying a container is
documented [here](https://cloud.google.com/compute/docs/containers/deploying-containers).

Maintaining the VM is a manual process that will likely involve performing upgrades to the VM and finding ways to
horizontally scale the application, all of which are non-trivial when working with individual VM instances.

Setting up internal IPs or internal DNS for service-to-service communication is done automatically, using the name of
the VM instance, hence no additional work is required. If running a web server, [load balancing](https://cloud.google.com/load-balancing/docs/how-to)
may have to be set up. There are simpler options for running containerized web servers.

Setting environment variables can be done by modifying `/etc/profile` on the VM instance.

Overall, getting a single VM up and running is fairly easy, where high-availability and scale are not required. This
option is being considered for building out an MVP.

For reference, Bitnami has provided options for single VM deployments.
 * [etcd](https://console.cloud.google.com/marketplace/details/bitnami-launchpad/etcd)
 * [kafka](https://console.cloud.google.com/marketplace/details/bitnami-launchpad/kafka)

#### Google Kubernetes Engine: Single Cluster with Node Pools
This involves creating a cluster and assigning applications to run on specific node pools. Applications are able to
communicate with each other directly at either the `Pod` or the `Service` level, through DNS-based [service discovery](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/).
`Pod` communication tends to be used when dealing with cluster configuration for a distributed application, potentially
requiring a headless `Service` to [establish network identity](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/),
if using `StatefulSet`. `Service` communication is more frequently used for round-robin load balancing of stateless
applications within the cluster.

Using a single cluster avoids having to configure an internal load balancer to expose services from other clusters
within the same VPC. It also has the advantage of reducing the cluster management fee, given that it's a fixed cost per
cluster. There may be disadvantages in terms of cluster isolation, but this requires further investigation. This option
currently seems to be the most viable.

#### Google Kubernetes Engine: Multiple Clusters
This involves creating a cluster for each application, which shares a lot of similarities with using a single cluster.
While there is more work to set up cluster-to-cluster networking, there is no need to manage multiple node pools and
which applications can be deployed across those node pools. 

#### Fully Managed
This is not applicable to all applications and is likely to vary in terms of feature set and pricing.

For reference, Confluent offers fully-managed solutions for [Kafka](https://console.cloud.google.com/marketplace/product/endpoints/payg-prod.gcpmarketplace.confluent.cloud).
Their implementation is agnostic to cloud platform but there is likely significant cost in migration and re-integrating
with different cloud platforms so there may not be much advantage in terms of avoiding vendor lock-in.
