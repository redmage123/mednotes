variable "audio_extraction_microservice_pod_name" {
  type    = string
  default = "audio-extraction-service"
}

variable "audio_extraction_microservice_container_name" {
  type    = string
  default = "audio-extraction-service"
}

variable "audio_extraction_microservice_image" {
  type    = string
  default = "audio_extraction_service-image:latest"
}

variable "audio_extraction_microservice_container_port" {
  type    = number
  default = 8002
}

variable "audio_extraction_microservice_command" {
  type    = list(string)
  default = ["python", "manage.py", "runserver", "0.0.0.0:8000"]
}

