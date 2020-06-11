data "template_file" "etcd_task_def" {
  template = file("${path.module}/templates/stock-config-task-def.json")

  vars = {
    filesystem_id = aws_efs_file_system.etcd.id
  }
}

resource "aws_efs_file_system" "etcd" {
  creation_token = "stock-config"

  tags = {
    Name = "stock-config"
  }
}

resource "aws_efs_mount_target" "etcd_east_2b" {
  file_system_id  = aws_efs_file_system.etcd.id
  subnet_id       = aws_subnet.east_2b.id
  security_groups = [aws_security_group.efs.id]
}

resource "aws_ecs_task_definition" "etcd" {
  family = "stock-config"

  container_definitions    = data.template_file.etcd_task_def.rendered
  requires_compatibilities = ["EC2"]
  network_mode             = "awsvpc"

  volume {
    name = "data-volume"

    efs_volume_configuration {
      file_system_id = aws_efs_file_system.etcd.id
    }
  }
}

resource "aws_ecs_service" "etcd" {
  name = "stock-config"

  cluster         = aws_ecs_cluster.default.arn
  task_definition = "${aws_ecs_task_definition.etcd.family}:${aws_ecs_task_definition.etcd.revision}"

  service_registries {
    registry_arn = aws_service_discovery_service.etcd.arn
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
    subnets          = [aws_subnet.east_2b.id]
    security_groups  = [aws_security_group.stock.id]
    assign_public_ip = false
  }
}

resource "aws_service_discovery_service" "etcd" {
  name         = "stock-config"
  namespace_id = aws_service_discovery_private_dns_namespace.stock.id

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.stock.id

    dns_records {
      ttl = 10
      type = "A"
    }
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}
