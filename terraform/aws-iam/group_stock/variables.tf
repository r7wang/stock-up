variable "path" {
  description = "Path for all resources created under this module"
}

variable "pass_roles" {
  description = "Roles that the group must be able to pass"
  type        = list(string)
}
