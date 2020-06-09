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
