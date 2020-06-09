resource "aws_iam_group" "default" {
  name = local.group
  path = var.path
}

resource "aws_iam_group_membership" "default" {
  name  = "${local.group}-membership"
  group = aws_iam_group.default.name
  users = [
    aws_iam_user.prod.name
  ]
}

resource "aws_iam_group_policy_attachment" "dynamodb" {
  group      = aws_iam_group.default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_group_policy_attachment" "ec2" {
  group      = aws_iam_group.default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

resource "aws_iam_group_policy_attachment" "ecs" {
  group      = aws_iam_group.default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonECS_FullAccess"
}

resource "aws_iam_group_policy_attachment" "s3" {
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

resource "aws_iam_group_policy" "ecs_service" {
  name   = "${local.group}-ecs-service"
  group  = aws_iam_group.default.name
  policy = data.aws_iam_policy_document.ecs_service.json
}

data "aws_iam_policy_document" "pass_role" {
  statement {
    effect    = "Allow"
    actions   = ["iam:PassRole"]
    resources = var.pass_roles
  }
}

resource "aws_iam_group_policy" "pass_role" {
  name   = "${local.group}-pass-role"
  group  = aws_iam_group.default.name
  policy = data.aws_iam_policy_document.pass_role.json
}
