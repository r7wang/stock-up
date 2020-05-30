variable "vm_depends_on" {
	type    = any
	default = null
}

variable "name" {}

variable "image" {}

variable "env" {
	type    = list(object({name=string, value=string}))
	default = null
}
