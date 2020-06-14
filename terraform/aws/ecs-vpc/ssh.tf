resource "aws_key_pair" "default" {
  key_name   = "ecs-ssh"
  public_key = file("ecs-ssh.pub")
}
