locals {
  namespace = kubernetes_namespace.prod.metadata[0].name
}

provider "kubernetes" {
  config_context = "stock"
}

resource "kubernetes_namespace" "prod" {
  metadata {
    name = "prod"
  }
}
