variable "vm_depends_on" {
  type    = any
  default = null
}

variable "name" {}

variable "machine_type" {
  type    = string
  default = "n1-standard-1"
}

variable "tags" {
  type    = list(string)
  default = null
}

variable "image" {}

variable "disk_size" {
  type    = number
  default = 10
}

variable "network" {
  type    = string
  default = "stock-network"
}

variable "subnetwork" {
  type    = string
  default = "default-us-east4"
}

variable "address" {
  type    = string
  default = null
}

variable "env" {
  type    = list(object({name=string, value=string}))
  default = null
}

output "vm_instance" {
  value = google_compute_instance.vm_instance
}
