resource "aws_iam_user" "prod" {
  name = "prod"
  path = "/stock/"
}

resource "aws_iam_access_key" "prod" {
  user = aws_iam_user.prod.name
}
