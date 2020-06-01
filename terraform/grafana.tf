module "stock-grafana" {
  source = "./gce-container"

  name  = "stock-grafana"
  image = "gcr.io/${var.project}/grafana:6.7.3"
  tags  = ["grafana", "allow-health_check"]

  env = [
    {
      name  = "GF_SECURITY_ADMIN_PASSWORD"
      value = var.grafana_password
    }
  ]
}
