module "stock_config" {
  source = "./ecs-container"

  name                           = "stock-config"
  image                          = "${local.ecr_repository}/etcd:3.4.7"
  task_definition_template       = "${path.module}/templates/stock-config-task-def.json"
  cluster_arn                    = aws_ecs_cluster.default.arn
  subnet_id                      = aws_subnet.east_2b.id
  ecs_security_group_id          = aws_security_group.stock.id
  efs_security_group_id          = aws_security_group.efs.id
  service_discovery_namespace_id = aws_service_discovery_private_dns_namespace.stock.id
}
