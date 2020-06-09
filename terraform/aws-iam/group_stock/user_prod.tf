resource "aws_iam_user" "prod" {
  name = local.environment
  path = var.path
}

resource "aws_iam_access_key" "prod" {
  user = aws_iam_user.prod.name
}
