module "stock_config" {
  source = "./gce-container"

  name  = "stock-config"
  image = "gcr.io/${var.project}/etcd:3.4.7"
  env = [
    {
      name = "ALLOW_NONE_AUTHENTICATION"
      value = "yes"
    }
  ]
}
