data "aws_ami" "default" {
  most_recent = true
  owners      = ["self", "amazon", "aws-marketplace"]

  filter {
    name   = "name"
    values = ["amzn-ami-*-amazon-ecs-optimized"]
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

data "template_file" "user_data" {
  template = file("${path.module}/templates/user-data.sh")

  vars = {
    cluster_name = aws_ecs_cluster.default.name
  }
}

resource "aws_key_pair" "default" {
  key_name   = "ecs-ssh"
  public_key = file("ecs-ssh.pub")
}

resource "aws_launch_template" "default" {
  name_prefix = "lt-${local.environment}-"

  instance_type          = "t3.micro"
  image_id               = join("", data.aws_ami.default.*.image_id)
  user_data              = base64encode(data.template_file.user_data.rendered)
  key_name               = aws_key_pair.default.key_name
  vpc_security_group_ids = [aws_security_group.stock.id]

  disable_api_termination              = false
  instance_initiated_shutdown_behavior = "terminate"


  block_device_mappings {
    device_name = join("", data.aws_ami.default.*.root_device_name)

    ebs {
      volume_type = "gp2"
      volume_size = 20
    }
  }

  credit_specification {
    cpu_credits = "standard"
  }

  iam_instance_profile {
    name = "ContainerInstanceRoleForEC2"
  }

  monitoring {
    enabled = true
  }
}
