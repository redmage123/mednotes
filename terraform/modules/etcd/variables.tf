variable "etcd_image" {
  type    = string
  default = "quay.io/coreos/etcd:latest"
}

variable "etcd_replicas" {
  type    = number
  default = 3
}

variable "etcd_storage_size" {
  type    = string
  default = "10Gi"
}

variable "etcd_storage_class_name" {
  type    = string
  default = "standard"
}

variable "app_image" {
  type    = string
  default = "my-image:latest"
}

variable "app_replicas" {
  type    = number
  default = 1
}

variable "app_port" {
  type    = number
  default = 8080
}

