resource "google_compute_ssl_certificate" "default" {
  name = "ssl-cert-default"

  private_key = file("default-key.pem")
  certificate = file("default-cert.pem")
}
