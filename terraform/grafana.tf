module "stock-grafana" {
  source = "./gce-container"

  name      = "stock-grafana"
  image     = "gcr.io/${var.project}/grafana:6.7.3"
  disk_size = 15
  tags      = ["grafana", "allow-health-check"]

  env = [
    {
      name  = "GF_SECURITY_ADMIN_PASSWORD"
      value = var.grafana_password
    }
  ]
}

resource "google_compute_instance_group" "grafana" {
  name = "ig-grafana"
  zone = "us-east4-c"

  instances = [module.stock-grafana.vm_instance.self_link]

  named_port {
    name = "grafana"
    port = "3000"
  }
}
