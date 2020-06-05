resource "kubernetes_ingress" "default" {
  metadata {
    name      = "stock-ingress"
    namespace = local.namespace

    annotations = {
      "kubernetes.io/ingress.allow-http" = "false"
    }
  }

  spec {
    tls {
      secret_name = "tls-cert"
    }

    backend {
      service_name = module.stock_grafana.service_name
      service_port = local.grafana_port
    }
  }
}