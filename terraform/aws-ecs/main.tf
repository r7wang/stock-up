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
  region = "us-east-2"
}

provider "aws" {
  version = "~> 2.0"

  region  = local.region
  profile = "prod"
}
