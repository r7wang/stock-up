terraform {
  backend "s3" {
    profile = "prod"

    # Handles state storage.
    bucket = "stock-up-terraform-state"
    key    = "prod/ecr/terraform.tfstate"
    region = "us-east-2"

    # Handles state locking.
    dynamodb_table = "stock-up-terraform-locks"
    encrypt        = true
  }
}

locals {
  environment    = "prod"
  region         = "us-east-2"
}

provider "aws" {
  version = "~> 2.0"

  profile = local.environment
  region  = local.region
}

module "etcd" {
  source = "./ecr-repository"

  name = "etcd"
}

module "zookeeper" {
  source = "./ecr-repository"

  name = "zookeeper"
}
