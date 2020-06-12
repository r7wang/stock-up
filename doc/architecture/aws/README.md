## AWS Concepts
This document seeks to simplify AWS concepts.

#### Burstable Instances
EC2 can deploy a variety of instance types, but certain instances types such as `T3`, `T3a` and `T2` instances are
burstable, which means that they consistently generate CPU credits at a set rate, and spend CPU credits to go above
their [baseline performance](https://aws.amazon.com/ec2/instance-types/t3/), which varies by instance type.

Instances can be configured to run with a `standard` or `unlimited` credit specification.
 * `standard` mode throttles the instance when there are no remaining CPU credits
 * `unlimited` mode offers fixed pricing for usage in excess of what is supported by CPU credits

#### AMI
These represent an image to be used with an EC2 instance.

AMIs can be found using a set of filters.
```hcl-terraform
data "aws_ami" "ecs_ami" {
  most_recent = true
  owners      = ["self", "amazon", "aws-marketplace"]

  filter {
    name   = "name"
    values = ["amzn-ami-*-amazon-ecs-optimized"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
```

AMIs can also be specified directly.
```hcl-terraform
data "aws_ami" "user_ami" {
  owners = ["self", "amazon", "aws-marketplace"]

  filter {
    name   = "image-id"
    values = ["ami-6944c513"]
  }
}
```

#### Security Groups
Firewall rules that are applied to any associated instances. Network interfaces on that instance are associated with
the default security group for the VPC, unless otherwise specified.

#### Launch Templates
These represent a preconfigured way to deploy new instances, including the following information.
 * AMI (`image_id`)
 * Instance type (`instance_type`)
 * Credit specification (`credit_specification`)
 * Boot disk (`block_device_mappings`)
 * Monitoring capabilities (`monitoring`)
 * Shutdown behavior (`instance_initiated_shutdown_behavior`)
 * Accidental termination protection (`disable_api_termination`)
 * Stores the role to be assumed by container instances (`iam_instance_profile`)
 * Security groups applied on a per-instance basis (`vpc_security_group_ids`)
 * Instance startup script (`user_data`)

## ECS Autoscaling
These are some of the relevant terms for understanding autoscaling concepts.
 * **ASG**: autoscaling group; defines scaling parameters for VM instances
 * **EC2**: elastic compute cloud; provides VM instances
 * **ECS**: elastic container service; runs container instances on VM instances
 * **Fargate**: abstracts provisioning and management of VM instances when running containers
 * **Scale-out**: action to increase the number of VM instances
 * **Scale-in**: action to decrease the number of VM instances

There are currently a few known approaches to autoscaling ECS.
 * Using ASG with scaling policies
 * Using ASG with ECS capacity providers
 * Using Fargate

### Using ASG with Scaling Policies
This requires creation of an ASG based on a launch template and defining the minimum, maximum, and desired number of
instances for a given instance type. ASGs can configure scaling policies that define the metrics that trigger scale-out
and scale-in actions. Metrics that would be used for scaling are likely going to be based on CPU/memory.

#### Advantages
 * N/A

#### Disadvantages
 * Scaling is primarily going to happen based on what's already running as opposed to what needs to be run, making the
   scaling behavior less efficient.
 * Scaling policies can be difficult to configure correctly.
 * There may be capacity at the cluster aggregate level, but no single instance has enough capacity to handle a task.
 * When scaling in, the ASG will pick an instance to terminate based on the termination policy. If the instance has
   running tasks, they will forcefully terminated resulting in a negative user experience. Note that this can be
   resolved using ASG lifecycle hooks and AWS Lambda as described [here](https://aws.amazon.com/blogs/compute/how-to-automate-container-instance-draining-in-amazon-ecs).
 * Scaling policies require tuning. 

### Using ASG with ECS Capacity Providers
This requires creation of an ASG just like the above, but without needing to configure scaling policies. A capacity
provider then has to be created to use this ASG. Scaling is based on outstanding tasks of a service and how much
additional capacity is required to run those tasks.

#### Advantages
 * This provides a fully managed experience to setting up scaling and takes care of challenges such as instance
   draining.
 * Scaling is application driven as opposed to infrastructure driven, making scaling behavior more efficient.

#### Disadvantages
 * Capacity providers are immutable and can't be deleted.
 * ASGs are permanently associated with the capacity provider. Modifying a capacity provider requires provisioning a
   new ASG with a unique name and migrating existing hosts to the new ASG.

#### Notes
 * This requires any given ASG to be within one availability zone, using one instance type, for fast scaling. Several
   ASGs are mixed together to form the capacity provider strategy. 

### Using Fargate
Setting up Fargate requires more investigation. Billing is based on the size of your container, regardless of what AWS
provisions under the hood.

#### Advantages
 * There is no need to manage any VM instances so more time to be devoted to the containers, tasks, and services.

#### Disadvantages
 * This uses a different pricing model and can be more expensive to run. 
 * Large containers launch much more slowly on Fargate, as opposed to EC2.
 * Sharing VM instances can be beneficial for on-disk caches that are used across multiple containers.
 * Logging and monitoring can be run once per VM instance instead of once per container.

## ECS Task Limits
Task limits on ECS depend on the EC2 instance types that are running, the amount of CPU, memory, and number of
interfaces supported. When `awsvpc` networking is used for tasks, the tasks consume a network interface. As per the
limits defined [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html), even instances up to
`t3.large` in size don't support more than 3 network interfaces, hence trying to run multiple tasks on a single host
might prove to be challenging.

Fortunately, there is a workaround through the use of [elastic network interface trunking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-eni.html),
which greatly increases the number of tasks that can be run on a given instance, as long as the instance supports this
mode of operation ([details](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-eni.html)).

## ECS Internet Access
Containers running under ECS that use `awsvpc` networking do not have access to the internet by default and must be
explicitly configured to do so through a NAT gateway. Details can be found [here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html).
