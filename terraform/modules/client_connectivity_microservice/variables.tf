variable "pod_name" {
  type = string
  default = "client-connectivity-service-pod"
}

variable "container_name" {
  type = string
  default = "client-connectivity-service-container"
}

variable "image" {
  type = string
  default = "client-connectivity-service-image:latest"
}

variable "container_port" {
  type = number
  default = 8001
}

variable "command" {
  type = list(string)
  default = ["python", "$client_connectivity_service_parent_path/manage.py", "runserver", "0.0.0.0:8000"]
}

variable "service_name" {
  type = string
  default = "client-connectivity-service"
}

variable "service_port" {
  type = number
  default = 8001
}

variable "service_type" {
  type = string
  default = "ClusterIP"
}

variable "labels" {
  type = map(string)
  default = {
    app = "client-connectivity-service"
  }
}

