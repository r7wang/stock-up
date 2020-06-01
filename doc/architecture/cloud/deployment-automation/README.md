## Deployment Automation
There are multiple tools that can help with cloud deployment.
 * provider UI
 * provider CLI
 * Terraform
 
### User Interface
The user interface tends to be very good for exploring cloud services and figuring out what resources are related to
each other, but after having this knowledge, it can become very tedious and error-prone. There are no good ways to
guarantee a reproducible deployment, short of extensive documentation.

### Command Line Interface
The command line tools are fairly robust and simple to use but potentially still error prone, given the significant
number of arguments associated with each command. Reproducible deployments can be scripted together, with the
additional advantage of easily running initialization scripts as part of the setup. This approach lacks the ability to
declaratively make piecemeal updates to the system.

### Terraform
Terraform supports all of the major cloud providers as well as many other services such as Kafka and etcd, through
third party providers. It's a very flexible declarative language that is very good at configuring the system towards a
desired state. Modules can also be built and shared to enable code reuse. One area where it struggles is in configuring
services through third party providers when there is no publicly facing IP to access the service. This problem may
still have to be resolved through the use of an initialization script (to be investigated).
