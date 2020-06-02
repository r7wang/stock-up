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

resource "google_compute_firewall" "allow_icmp" {
  name        = "allow-icmp"
  description = "Allow ICMP from anywhere"

  network = google_compute_network.stock_network.id

  allow {
   protocol = "icmp"
  }
}

resource "google_compute_firewall" "allow_internal" {
  name        = "allow-internal"
  description = "Allow all internal traffic"

  network       = google_compute_network.stock_network.id
  source_ranges = ["10.128.0.0/9"]

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "icmp"
  }
}

resource "google_compute_firewall" "allow_ssh" {
  name        = "allow-ssh"
  description = "Allow SSH from anywhere"

  network = google_compute_network.stock_network.id

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}
