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
    request_path = "/"
  }
}
