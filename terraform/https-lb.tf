resource "google_compute_global_forwarding_rule" "grafana" {
  name = "gfr-grafana"

  target     = google_compute_target_https_proxy.grafana.id
  ip_address = google_compute_global_address.grafana.address
  port_range = "443"
  depends_on = [google_compute_global_address.grafana]
}

resource "google_compute_global_address" "grafana" {
  name = "external-address-grafana"

  address_type = "EXTERNAL"
  ip_version   = "IPV4"
}

resource "google_compute_target_https_proxy" "grafana" {
  name = "target-https-grafana"

  url_map          = google_compute_url_map.grafana.id
  ssl_certificates = [google_compute_ssl_certificate.default.id]
}

resource "google_compute_url_map" "grafana" {
  name = "urlmap-grafana"

  default_service = google_compute_backend_service.grafana.id
}

resource "google_compute_backend_service" "grafana" {
  name = "backend-grafana"

  backend {
    group = google_compute_instance_group.grafana.self_link
  }

  protocol  = "HTTP"
  port_name = "grafana"

  health_checks = [google_compute_health_check.grafana.id]
}

resource "google_compute_health_check" "grafana" {
  name = "health-check-grafana"

  check_interval_sec  = 10
  timeout_sec         = 5
  healthy_threshold   = 2
  unhealthy_threshold = 3

  http_health_check {
    port         = 3000
    request_path = "/api/health"
  }
}

resource "google_compute_firewall" "allow_health_check" {
  name        = "allow-health-check"
  description = "Allow health check from load balancer IP ranges"

  network       = google_compute_network.stock_network.id
  source_ranges = ["130.211.0.0/22", "35.191.0.0/16"]
  target_tags   = ["allow-health-check"]

  allow {
    protocol = "tcp"
    ports    = ["80", "3000"]
  }
}
