# Define the Kubernetes provider
provider "kubernetes" {}

# Define the etcd stateful set
resource "kubernetes_stateful_set" "etcd" {
  metadata {
    name = "etcd"
  }

  spec {
    selector {
      match_labels = {
        app = "etcd"
      }
    }

    service_name = "etcd"
    replicas     = var.etcd_replicas

    template {
      metadata {
        labels = {
          app = "etcd"
        }
      }

      spec {
        container {
          image = var.etcd_image

          name  = "etcd"
          ports {
            container_port = 2379
            name           = "client"
          }

          command = ["/usr/local/bin/etcd"]
          args    = [
            "--name", "${count.index}",
            "--data-dir", "/var/run/etcd",
            "--listen-client-urls", "http://0.0.0.0:2379",
            "--advertise-client-urls", "http://${self.pod_ip}:2379",
            "--initial-advertise-peer-urls", "http://${self.pod_ip}:2380",
            "--listen-peer-urls", "http://0.0.0.0:2380",
            "--initial-cluster", "etcd-0=http://etcd-0.etcd:2380,etcd-1=http://etcd-1.etcd:2380,etcd-2=http://etcd-2.etcd:2380",
            "--initial-cluster-state", "new",
            "--initial-cluster-token", "etcd-token"
          ]
        }
      }
    }

    volume_claim_template {
      metadata {
        name = "etcd-data"
      }

      spec {
        access_modes = ["ReadWriteOnce"]
        resources {
          requests {
            storage = var.etcd_storage_size
          }
        }

        storage_class_name = var.etcd_storage_class_name
      }
    }
  }
}

# Define the etcd service
resource "kubernetes_service" "etcd" {
  metadata {
    name = "etcd"
  }

  spec {
    selector = {
      app = "etcd"
    }

    port {
      port        = 2379
      target_port = "client"
    }

    type = "ClusterIP"
  }
}

# Define the application deployment
resource "kubernetes_deployment" "app" {
  metadata {
    name = "app"
  }

  spec {
    selector {
      match_labels = {
        app = "app"
      }
    }

    replicas = var.app_replicas

    template {
      metadata {
        labels = {
          app = "app"
        }
      }

      spec {
        container {
          image = var.app_image

          name  = "app"
          ports {
            container_port = 8080
            name           = "http"
          }

          env {
            name  = "ETCD_SERVERS"
            value = "${join(",", kubernetes_stateful_set.etcd.*.status.0.pod_ip)}"
          }

          args = ["--port=8080"]
        }
      }
    }
  }
}

# Define the application service
resource "kubernetes_service" "app" {
  metadata {
    name = "app"
  }

  spec {
    selector = {
      app = "app"
    }

    port {
      port        = 8080
      target_port = "http"
    }

    type = "ClusterIP"
  }
}
container {
  image = "my-image:latest"

  name  = "app"
  ports {
    container_port = 8080
    name           = "http"
  }

  env {
    name  = "ETCD_SERVERS"
    value = "${join(",", kubernetes_stateful_set.etcd.*.status.0.pod_ip)}"
  }

  command = ["./my-app"]
}

