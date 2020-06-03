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
