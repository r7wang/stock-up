locals {
  labels = {
    "release"                = var.release
    "app.kubernetes.io/name" = var.release
  }
}

resource "kubernetes_stateful_set" "default" {
  metadata {
    name      = "${var.release}-statefulset"
    namespace = var.namespace
    labels    = local.labels
  }

  spec {
    selector {
      match_labels = local.labels
    }
    service_name          = kubernetes_service.headless.metadata[0].name
    pod_management_policy = "OrderedReady"
    replicas              = 1

    template {
      metadata {
        name = "${var.release}-statefulset-template"
        labels = local.labels
      }

      spec {
        security_context {
          run_as_user     = 1001
          fs_group        = 1001
        }

        container {
          name              = "${var.release}-container"
          image             = var.image
          image_pull_policy = "IfNotPresent"

          resources {
            requests {
              cpu    = "100m"
              memory = "1Gi"
            }

            limits {
              cpu    = "200m"
              memory = "1Gi"
            }
          }

          volume_mount {
            name       = "${var.release}-volumeclaim-data"
            mount_path = var.mount_path
          }

          dynamic "env" {
            for_each = var.env
            content {
              name = env.value.name
              value = env.value.value
            }
          }

          dynamic "port" {
            for_each = var.ports
            content {
              name = port.value.name
              container_port = port.value.port
            }
          }

          liveness_probe {
            tcp_socket {
              port = "client"
            }
            initial_delay_seconds = 10
            period_seconds = 10
            timeout_seconds = 5
            success_threshold = 1
            failure_threshold = 2
          }

          readiness_probe {
            tcp_socket {
              port = "client"
            }
            initial_delay_seconds = 15
            period_seconds = 10
            timeout_seconds = 5
            success_threshold = 1
            failure_threshold = 6
          }
        }
      }
    }

    update_strategy {
      type = "RollingUpdate"

      rolling_update {
        partition = 0
      }
    }

    volume_claim_template {
      metadata {
        name      = "${var.release}-volumeclaim-data"
        namespace = var.namespace
        labels    = local.labels
      }

      spec {
        access_modes       = ["ReadWriteOnce"]
        storage_class_name = kubernetes_storage_class.default.metadata[0].name

        resources {
          requests = {
            storage = "1Gi"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "headless" {
  metadata {
    name      = "${var.release}-svc-headless"
    namespace = var.namespace
    labels    = local.labels
  }

  spec {
    type       = "ClusterIP"
    cluster_ip = "None"
    selector   = local.labels

    dynamic "port" {
      for_each = var.ports
      content {
        name = port.value.name
        port = port.value.port
        target_port = port.value.name
      }
    }
  }
}

resource "kubernetes_storage_class" "default" {
  metadata {
    name   = "${var.release}-storageclass-ssd"
    labels = local.labels
  }

  storage_provisioner = "kubernetes.io/gce-pd"
  parameters = {
    type = "pd-ssd"
  }
}
