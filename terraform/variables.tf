variable "client_connectivity_service_pod_name" {
  type    = string
  default = "client-connectivity-service"
}

variable "client_connectivity_service_container_name" {
  type    = string
  default = "client-connectivity-service"
}

variable "client_connectivity_service_image" {
  type    = string
  default = "client-connectivity-service-image:latest"
}

variable "client_connectivity_service_container_port" {
  type    = number
  default = 8000
}

variable "client_connectivity_service_command" {
  type    = list(string)
  default = ["python", "$client_connectivity_service_parent_path/manage.py", "runserver", "0.0.0.0:8000"]
}

variable "client_connectivity_service_service_name" {
  type    = string
  default = "client-connectivity-service"
}

variable "client_connectivity_service_service_port" {
  type    = number
  default = 8000
}

variable "client_connectivity_service_service_type" {
  type    = string
  default = "ClusterIP"
}

