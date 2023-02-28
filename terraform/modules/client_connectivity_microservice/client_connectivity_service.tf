resource "kubernetes_pod" "client_connectivity_service_pod" {
  metadata {
    name = var.client_connectivity_service_pod_name
  }

  spec {
    container {
      name  = var.client_connectivity_service_container_name
      image = var.client_connectivity_service_image

      port {
        name = "http"
        container_port = var.client_connectivity_service_container_port
      }   

      command = var.client_connectivity_service_command
    }   
  }
}

resource "kubernetes_service" "client_connectivity-service" {

  metadata {
    name = var.client_connectivity_service_container_name
  }

  spec {
    selector = { 
      app = var.client_connectivity_service_container_name
    }   

    port {
      name = "http"
      port = var.client_connectivity_service_container_port
      target_port = "http"
    }   

    type = "ClusterIP"
  }
}

