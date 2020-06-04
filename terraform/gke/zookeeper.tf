locals {
  zookeeper_port = 2181
}

module "stock_zookeeper" {
  source = "./stateful-service"

  namespace  = local.namespace
  release    = "stock-zookeeper"
  image      = "gcr.io/${var.project}/zookeeper:3.6.1"
  mount_path = "/bitnami/zookeeper"

  ports = [
    {
      name = "client"
      port = local.zookeeper_port
    }
  ]

  env = [
    {
      name  = "ALLOW_ANONYMOUS_LOGIN"
      value = "yes"
    }
  ]
}
