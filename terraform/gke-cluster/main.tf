provider "google" {
  version = "3.5.0"

  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

resource "google_container_cluster" "stock" {
  name        = "stock-cluster"
  description = "Cluster shared across all services"

  location                 = "us-east4-c"
  remove_default_node_pool = true
  initial_node_count       = 1
  network                  = google_compute_network.stock_network.id
  subnetwork               = google_compute_subnetwork.us_east4.id

  ip_allocation_policy {}
}

resource "google_container_node_pool" "stock" {
  name = "stock-nodes"

  location   = "us-east4-c"
  cluster    = google_container_cluster.stock.name
  node_count = 3

  node_config {
    disk_size_gb = 20
    machine_type = "n1-standard-1"

    metadata = {
      disable-legacy-endpoints = "true"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}
