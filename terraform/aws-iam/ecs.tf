/*
# ECS service permissions (legacy, no longer required).
data "aws_iam_policy_document" "ecs_service_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ecs.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "ecs_service" {
  name               = "ServiceRoleForECS"
  path               = "/stock/"
  assume_role_policy = data.aws_iam_policy_document.ecs_service_assume_role.json
}

resource "aws_iam_role_policy_attachment" "ecs_service" {
  role       = aws_iam_role.ecs_service.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceRole"
}
*/
