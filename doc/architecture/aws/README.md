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
 * Instance name (`key_name`)
 * AMI (`image_id`)
 * Instance type (`instance_type`)
 * Credit specification (`credit_specification`)
 * Boot disk (`block_device_mappings`)
 * Monitoring capabilities (`monitoring`)
 * Shutdown behavior (`instance_initiated_shutdown_behavior`)
 * Accidental termination protection (`disable_api_termination`)
 * ??? (`iam_instance_profile`)
 * ??? (`vpc_security_group_ids`)
 * ??? (`user_data`)
