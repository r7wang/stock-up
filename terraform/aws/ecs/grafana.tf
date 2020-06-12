module "stock_grafana" {
  source = "./ecs-container"

  name                           = "stock-grafana"
  image                          = "${local.ecr_repository}/grafana:6.7.3"
  admin_password                 = var.grafana_password
  task_definition_template       = "${path.module}/templates/stock-grafana-task-def.json"
  cluster_arn                    = aws_ecs_cluster.default.arn
  subnet_id                      = data.aws_subnet.east_2b.id
  ecs_security_group_id          = data.aws_security_group.stock.id
  efs_security_group_id          = data.aws_security_group.efs.id
  service_discovery_namespace_id = aws_service_discovery_private_dns_namespace.stock.id
}
