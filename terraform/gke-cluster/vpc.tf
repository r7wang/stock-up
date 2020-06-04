resource "google_compute_network" "stock_network" {
  name = "stock-network"

  auto_create_subnetworks = "false"
  routing_mode            = "REGIONAL"
}

resource "google_compute_subnetwork" "us_east4" {
  name = "default-us-east4"

  network       = google_compute_network.stock_network.id
  region        = "us-east4"
  ip_cidr_range = "10.128.0.0/20"
}
