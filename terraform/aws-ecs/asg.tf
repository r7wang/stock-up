resource "aws_autoscaling_group" "default" {
  name = "asg-${aws_launch_template.default.id}"

  launch_template {
    id      = aws_launch_template.default.id
    version = "$Latest"
  }

  min_size                  = 1
  max_size                  = 1
  desired_capacity          = 1
  health_check_type         = "EC2"
  health_check_grace_period = 600
  termination_policies      = ["Default"]

  vpc_zone_identifier = [
    aws_subnet.east_2a.id,
    aws_subnet.east_2b.id,
    aws_subnet.east_2c.id,
  ]

  enabled_metrics = [
    "GroupMinSize",
    "GroupMaxSize",
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupPendingInstances",
    "GroupStandbyInstances",
    "GroupTerminatingInstances",
    "GroupTotalInstances",
  ]

  tag {
    key                 = "Name"
    value               = "ContainerInstance"
    propagate_at_launch = true
  }

  tag {
    key                 = "Project"
    value               = local.project
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = local.environment
    propagate_at_launch = true
  }
}
