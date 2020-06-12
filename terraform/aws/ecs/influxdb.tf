module "stock_influxdb" {
  source = "./ecs-container"

  name                           = "stock-influxdb"
  image                          = "${local.ecr_repository}/influxdb:1.8.0"
  admin_password                 = var.influxdb_password
  task_definition_template       = "${path.module}/templates/stock-influxdb-task-def.json"
  cluster_arn                    = aws_ecs_cluster.default.arn
  subnet_id                      = data.aws_subnet.east_2b.id
  ecs_security_group_id          = data.aws_security_group.stock.id
  efs_security_group_id          = data.aws_security_group.efs.id
  service_discovery_namespace_id = aws_service_discovery_private_dns_namespace.stock.id
}
