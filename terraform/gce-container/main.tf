module "container-vm" {
  source  = "terraform-google-modules/container-vm/google"
  version = "2.0.0"

  container = {
    image = var.image
    env = var.env
  }

  restart_policy = "Always"
}

resource "google_compute_instance" "vm_instance" {
  depends_on = [var.vm_depends_on]

  name         = var.name
  machine_type = "n1-standard-1"

  allow_stopping_for_update = "true"

  boot_disk {
    initialize_params {
      image = module.container-vm.source_image
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  metadata = {
    gce-container-declaration = module.container-vm.metadata_value
    google-logging-enabled    = "true"
    google-monitoring-enabled = "true"
  }

  labels = {
    container-vm = module.container-vm.vm_container_label
  }

  service_account {
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}
