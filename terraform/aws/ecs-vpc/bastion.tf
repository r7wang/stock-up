data "aws_ami" "bastion" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-*-gp2"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "bastion" {
  ami                    = join("", data.aws_ami.bastion.*.image_id)
  availability_zone      = "us-east-2b"
  instance_type          = "t3.nano"
  key_name               = aws_key_pair.default.key_name
  subnet_id              = aws_subnet.public_east_2b.id
  vpc_security_group_ids = [aws_security_group.stock.id]

  tags = {
    Name = "BastionInstance"
  }
}
