data "template_file" "task_def" {
  template = file(var.task_definition_template)

  vars = {
    name           = var.name
    image          = var.image
    admin_password = var.admin_password
  }
}

resource "aws_efs_file_system" "default" {
  creation_token = var.name

  tags = {
    Name = var.name
  }
}

resource "aws_efs_mount_target" "east_2b" {
  file_system_id  = aws_efs_file_system.default.id
  subnet_id       = var.subnet_id
  security_groups = [var.efs_security_group_id]
}

resource "aws_ecs_task_definition" "default" {
  family = var.name

  container_definitions    = data.template_file.task_def.rendered
  requires_compatibilities = ["EC2"]
  network_mode             = "awsvpc"

  volume {
    name = "data-volume"

    efs_volume_configuration {
      file_system_id = aws_efs_file_system.default.id
    }
  }
}

resource "aws_ecs_service" "default" {
  name = var.name

  cluster         = var.cluster_arn
  task_definition = "${aws_ecs_task_definition.default.family}:${aws_ecs_task_definition.default.revision}"

  service_registries {
    registry_arn = aws_service_discovery_service.default.arn
  }

  launch_type                        = "EC2"
  scheduling_strategy                = "REPLICA"
  desired_count                      = 1
  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 100

  deployment_controller {
    type = "ECS"
  }

  network_configuration {
    subnets          = [var.subnet_id]
    security_groups  = [var.ecs_security_group_id]
    assign_public_ip = false
  }

  depends_on = [aws_efs_mount_target.east_2b]
}

resource "aws_service_discovery_service" "default" {
  name         = var.name
  namespace_id = var.service_discovery_namespace_id

  dns_config {
    namespace_id = var.service_discovery_namespace_id

    dns_records {
      ttl = 10
      type = "A"
    }
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}