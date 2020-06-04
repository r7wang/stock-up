variable "namespace" {}

variable "release" {}

variable "image" {}

variable "env" {
  type    = list(object({name=string, value=string}))
  default = null
}

