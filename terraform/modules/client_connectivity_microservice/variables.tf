variable "client_connectivity_service_pod_name" {
  type = string
  default = "client_connectivity-service"
}

variable "client_connectivity_service_container_name" {
  type = string
  default = "client_connectivity-service"
}

variable "client_connectivity_service_image" {
  type = string
  default = "client_connectivity_service-image:latest"
}

variable "client_connectivity_service_container_port" {
  type = number
  default = 8001
}

variable "client_connectivity_service_command" {
  type = list(string)
  default = ["python", "-m", "client_connectivity_service"]
}

variable "client_connectivity_service_name" {
  type = string
  default = "client_connectivity-service"
}

variable "client_connectivity_service_port" {
  type = number
  default = 8001
}

variable "client_connectivity_service_type" {
  type = string
  default = "ClusterIP"
}

