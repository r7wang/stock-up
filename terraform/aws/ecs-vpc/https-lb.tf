resource "aws_lb" "default" {
  name               = "lb-stock"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.stock.id]
  subnets            = [aws_subnet.public_east_2a.id, aws_subnet.public_east_2b.id]

  tags = {
    Name = "lb-stock"
  }
}

resource "aws_lb_listener" "default" {
  load_balancer_arn = aws_lb.default.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.default.arn
  }
}

resource "aws_lb_target_group" "default" {
  name        = "lb-tg-stock"
  port        = 3000
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.stock.id

  tags = {
    Name = "lb-tg-stock"
  }
}
