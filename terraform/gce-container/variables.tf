variable "vm_depends_on" {
	type    = any
	default = null
}

variable "name" {}

variable "image" {}

variable "disk_size" {
    type    = number
    default = 10
}

variable "env" {
	type    = list(object({name=string, value=string}))
	default = null
}
