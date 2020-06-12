locals {
  path = "/stock/"
}

provider "aws" {
  version = "~> 2.0"

  region  = "us-east-2"
  profile = "security"
}

data "aws_iam_group" "security" {
  group_name = "security"
}

data "aws_iam_user" "admin_security" {
  user_name = "admin_security"
}

module "group_stock" {
  source = "./group_stock"

  path  = local.path
  pass_roles = [
    aws_iam_role.container_instance_ec2.arn,
  ]
}
