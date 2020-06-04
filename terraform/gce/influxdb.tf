module "stock_influxdb" {
  source = "./gce-container"

  name  = "stock-influxdb"
  image = "gcr.io/${var.project}/influxdb:1.8.0"
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
