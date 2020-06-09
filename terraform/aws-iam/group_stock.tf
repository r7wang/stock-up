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

resource "aws_iam_group_policy_attachment" "stock_group_ec2" {
  group      = aws_iam_group.default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

resource "aws_iam_group_policy_attachment" "stock_group_ecs" {
  group      = aws_iam_group.default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonECS_FullAccess"
}

resource "aws_iam_group_policy_attachment" "stock_group_s3" {
  group      = aws_iam_group.default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

data "aws_iam_policy_document" "ecs_service" {
  statement {
    effect    = "Allow"
    actions   = ["iam:CreateServiceLinkedRole"]
    resources = ["arn:aws:iam::*:role/aws-service-role/ecs.amazonaws.com/AWSServiceRoleForECS*"]

    condition {
      test     = "StringLike"
      variable = "iam:AWSServiceName"
      values   = ["ecs.amazonaws.com"]
    }
  }
}

resource "aws_iam_group_policy" "stock_group_ecs_service" {
  name   = "stock-group-ecs-service"
  group  = aws_iam_group.default.name
  policy = data.aws_iam_policy_document.ecs_service.json
}
