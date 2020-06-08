provider "google" {
  version = "3.5.0"

  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

resource "google_storage_bucket" "terraform_state" {
  name = "stock-up-terraform-state"

  versioning {
    enabled = true
  }
}
