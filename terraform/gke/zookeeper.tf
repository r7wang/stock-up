module "stock-zookeeper" {
  source = "./stateful-service"

  namespace  = kubernetes_namespace.prod.metadata[0].name
  release    = "stock-zookeeper"
  image      = "gcr.io/${var.project}/zookeeper:3.6.1"
  mount_path = "/bitnami/zookeeper"

  ports = [
    {
      name = "client"
      port = 2181
    }
  ]

  env = [
    {
      name  = "ALLOW_ANONYMOUS_LOGIN"
      value = "yes"
    }
  ]
}
