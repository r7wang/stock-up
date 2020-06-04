locals {
  labels = {
    "release"                = var.release
    "app.kubernetes.io/name" = var.release
  }
}

resource "kubernetes_deployment" "default" {
  metadata {
    name      = "${var.release}-deployment"
    namespace = var.namespace
    labels    = local.labels
  }

  spec {
    selector {
      match_labels = local.labels
    }
    replicas = 1

    template {
      metadata {
        name      = "${var.release}-deployment-template"
        namespace = var.namespace
        labels    = local.labels
      }

      spec {
        container {
          name              = "${var.release}-container"
          image             = var.image
          image_pull_policy = "IfNotPresent"

          resources {
            requests {
              cpu    = "100m"
              memory = "500Mi"
            }

            limits {
              cpu    = "200m"
              memory = "1Gi"
            }
          }

          dynamic "env" {
            for_each = var.env
            content {
              name = env.value.name
              value = env.value.value
            }
          }

          liveness_probe {
            exec {
              command = ["echo", "0"]
            }
          }

          readiness_probe {
            exec {
              command = ["echo", "0"]
            }
          }
        }
      }
    }
  }
}
