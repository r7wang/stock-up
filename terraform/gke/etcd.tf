module "stock-config" {
  source = "./stateful-service"

  namespace  = kubernetes_namespace.prod.metadata[0].name
  release    = "stock-config"
  image      = "gcr.io/${var.project}/etcd:3.4.7"
  mount_path = "/bitnami/etcd"

  ports = [
    {
      name = "client"
      port = 2379
    },
    {
      name = "peer"
      port = 2380
    }
  ]

  env = [
    {
      name  = "ALLOW_NONE_AUTHENTICATION"
      value = "yes"
    }
  ]
}
