variable "name" {
  description = "Name of the deployment"
}

variable "task_definition_template" {
  description = "Path where the task definition template can be found"
}

variable "image" {
  description = "Container image to use"
}

variable "cluster_arn" {}

variable "subnet_id" {}

variable "ecs_security_group_id" {}

variable "efs_security_group_id" {}

variable "service_discovery_namespace_id" {}
