oresource "kubernetes_pod" "audio_extraction_microservice_pod" {
  metadata {
    name = var.audio_extraction_microservice_pod_name
  }

  spec {
    container {
      name  = var.audio_extraction_microservice_container_name
      image = var.audio_extraction_microservice_image

      port {
        name          = "http"
        container_port = var.audio_extraction_microservice_container_port
      }

      command = var.audio_extraction_microservice_command
    }
  }
}

