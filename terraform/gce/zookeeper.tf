module "stock_zookeeper" {
  source = "./gce-container"

  name  = "stock-zookeeper"
  image = "gcr.io/${var.project}/zookeeper:3.6.1"
  env = [
    {
      name  = "ALLOW_ANONYMOUS_LOGIN"
      value = "yes"
    }
  ]
}
