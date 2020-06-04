resource "kubernetes_ingress" "default" {
  metadata {
    name      = "stock-ingress"
    namespace = local.namespace
  }

  spec {
    backend {
      service_name = module.stock_grafana.service_name
      service_port = local.grafana_port
    }
  }
}