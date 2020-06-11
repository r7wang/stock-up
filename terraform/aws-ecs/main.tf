terraform {
  backend "s3" {
    profile = "prod"

    # Handles state storage.
    bucket = "stock-up-terraform-state"
    key    = "prod/ecs/terraform.tfstate"
    region = "us-east-2"

    # Handles state locking.
    dynamodb_table = "stock-up-terraform-locks"
    encrypt        = true
  }
}

locals {
  environment    = "prod"
  region         = "us-east-2"
  project        = "stock-up"
  ecr_repository = "${var.account}.dkr.ecr.${local.region}.amazonaws.com"
}

provider "aws" {
  version = "~> 2.0"

  profile = local.environment
  region  = local.region
}
