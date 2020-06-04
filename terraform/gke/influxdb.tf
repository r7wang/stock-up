locals {
  influxdb_port = 8086
}

module "stock_influxdb" {
  source = "./stateful-service"

  namespace  = local.namespace
  release    = "stock-influxdb"
  image      = "gcr.io/${var.project}/influxdb:1.8.0"
  mount_path = "/bitnami/influxdb"

  ports = [
    {
      name = "client"
      port = local.influxdb_port
    },
  ]

  env = [
    {
      name  = "INFLUXDB_HTTP_AUTH_ENABLED"
      value = "true"
    },
    {
      name  = "INFLUXDB_ADMIN_USER"
      value = "admin"
    },
    {
      name  = "INFLUXDB_ADMIN_USER_PASSWORD"
      value = var.influxdb_password
    }
  ]
}
