provider "kubernetes" {
  config_context = "stock"
}

resource "kubernetes_namespace" "prod" {
  metadata {
    name = "prod"
  }
}
