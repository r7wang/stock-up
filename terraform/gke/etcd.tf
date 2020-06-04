module "stock_config" {
  source = "./stateful-service"

  namespace  = local.namespace
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

  tcp_probes = [
    {
      port_name = "client"
    }
  ]

  env = [
    {
      name  = "ALLOW_NONE_AUTHENTICATION"
      value = "yes"
    }
  ]
}
