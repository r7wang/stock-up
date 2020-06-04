locals {
  grafana_port = 3000
}

module "stock_grafana" {
  source = "./stateful-service"

  namespace  = local.namespace
  release    = "stock-grafana"
  image      = "gcr.io/${var.project}/grafana:6.7.3"
  mount_path = "/opt/bitnami/grafana/data"
  neg_status = jsonencode(
    {
      network_endpoint_groups: {
        3000: "k8s1-830769d5-prod-stock-grafana-svc-3000-393100fd"
      }
      zones: ["us-east4-c"]
    }
  )

  ports = [
    {
      name = "client"
      port = local.grafana_port
    },
  ]

  http_probes = [
    {
      path      = "/api/health"
      port_name = "client"
    }
  ]

  env = [
    {
      name  = "GF_SECURITY_ADMIN_PASSWORD"
      value = var.grafana_password
    }
  ]
}
