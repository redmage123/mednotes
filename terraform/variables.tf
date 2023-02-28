variable "client_connectivity_service_pod_name" {
  type = string
  default = "client_connectivity-service"
}

variable "nginx_pod_name" {
  type = string
  default = "nginx"
}

variable "pod_names" {
  type = list(string)
  default = ["client_connectivity_service", "nginx"]
}

variable "client_connectivity_service_pod_labels" {
  type = map(string)
  default = { 
    app = "client_connectivity-service"
  }
}

variable "nginx_pod_labels" {
  type = map(string)
  default = { 
    app = "nginx"
  }
}

variable "pod_labels" {
  type = map(map(string))
  default = { 
    "client_connectivity_service" = {
      app = "client_connectivity_service"
    },
    "nginx" = {
      app = "nginx"
    }
  }
}

variable "nginx_container_name" {
  type = string
  default = "nginx-container"
}

variable "nginx_image" {
  type = string
  default = "nginx:latest"
}

variable "nginx_container_port" {
  type = number
  default = 8081
}

variable "nginx_service_name" {
  type = string
  default = "nginx-service"
}

variable "nginx_service_port" {
  type = number
  default = 8081
}

variable "nginx_service_type" {
  type = string
  default = "ClusterIP"
}

variable "nginx_config_file" {
  type = string
  default = "/home/bbrelin/src/repos/mednotes/src/config/nginx.conf"
}



variable "client_connectivity_service_container_name" {
  type = string
  default = "client_connectivity-service"
}

variable "client_connectivity_service_image" {
  type = string
  default = "python:3.10-alpine"
}

variable "client_connectivity_service_container_port" {
  type = number
  default = 8001
}

variable "client_connectivity_service_command" {
  type = list(string)
  default = ["python", "-m", "client_connectivity_service"]
}

variable "client_connectivity_service_service_name" {
  type = string
  default = "client_connectivity_service"
}

variable "client_connectivity_service_service_port" {
  type = number
  default = 8001
}

variable "client_connectivity_service_service_type" {
  type = string
  default = "ClusterIP"
}

