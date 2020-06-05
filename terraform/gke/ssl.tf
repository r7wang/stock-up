resource "kubernetes_secret" "tls_cert" {
  metadata {
    name      = "tls-cert"
    namespace = local.namespace
  }

  data = {
    "tls.crt" = file("default-cert.pem")
    "tls.key" = file("default-key.pem")
  }

  type = "kubernetes.io/tls"
}