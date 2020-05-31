variable "vm_depends_on" {
	type    = any
	default = null
}

variable "name" {}

variable "tags" {
	type    = list(string)
	default = null
}

variable "image" {}

variable "disk_size" {
    type    = number
    default = 10
}

variable "address" {
	type    = string
	default = null
}

variable "env" {
	type    = list(object({name=string, value=string}))
	default = null
}
