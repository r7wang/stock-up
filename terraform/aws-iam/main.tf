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

resource "aws_iam_group" "default" {
  name = "stock-group"
  path = "/stock/"
}

resource "aws_iam_group_membership" "default" {
  name  = "stock-group-membership"
  group = aws_iam_group.default.name
  users = [
    aws_iam_user.prod.name
  ]
}

resource "aws_iam_group_policy_attachment" "stock_group_dynamodb" {
  group      = aws_iam_group.default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_group_policy_attachment" "stock_group_ecs" {
  group      = aws_iam_group.default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonECS_FullAccess"
}

resource "aws_iam_group_policy_attachment" "stock_group_s3" {
  group      = aws_iam_group.default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_user" "prod" {
  name = "prod"
  path = "/stock/"
}

resource "aws_iam_access_key" "prod" {
  user = aws_iam_user.prod.name
}
