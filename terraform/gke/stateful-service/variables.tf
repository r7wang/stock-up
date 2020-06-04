variable "namespace" {}

variable "release" {}

variable "image" {}

variable "mount_path" {}

variable "ports" {
  type    = list(object({name=string, port=number}))
  default = null
}

variable "env" {
  type    = list(object({name=string, value=string}))
  default = null
}

variable "tcp_probes" {
  type    = list(object({port_name=string}))
  default = []
}

variable "http_probes" {
  type    = list(object({path=string, port_name=string}))
  default = []
}

variable "neg_status" {
  default = null
}

output "service_name" {
  value = kubernetes_service.default.metadata[0].name
}
