locals {
  release = "stock-config"
  labels = {
    "release"                = local.release
    "app.kubernetes.io/name" = local.release
  }
}

resource "kubernetes_stateful_set" "etcd" {
  metadata {
    name      = "${local.release}-statefulset"
    namespace = kubernetes_namespace.prod.metadata[0].name
    labels    = local.labels
  }

  spec {
    selector {
      match_labels = local.labels
    }
    service_name          = kubernetes_service.etcd_headless.metadata[0].name
    pod_management_policy = "OrderedReady"
    replicas              = 1

    template {
      metadata {
        name = "${local.release}-statefulset-template"
        labels = local.labels
      }

      spec {
        security_context {
          run_as_user     = 1001
          fs_group        = 1001
        }

        container {
          name              = "${local.release}-container"
          image             = "gcr.io/${var.project}/etcd:3.4.7"
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
            name       = "${local.release}-volumeclaim-data"
            mount_path = "/bitnami/etcd"
          }

          env {
            name  = "ALLOW_NONE_AUTHENTICATION"
            value = "yes"
          }

          port {
            name           = "client"
            container_port = 2379
          }

          port {
            name           = "peer"
            container_port = 2380
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
        name      = "${local.release}-volumeclaim-data"
        namespace = kubernetes_namespace.prod.metadata[0].name
        labels    = local.labels
      }

      spec {
        access_modes       = ["ReadWriteOnce"]
        storage_class_name = kubernetes_storage_class.etcd.metadata[0].name

        resources {
          requests = {
            storage = "1Gi"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "etcd_headless" {
  metadata {
    name      = "${local.release}-svc-headless"
    namespace = kubernetes_namespace.prod.metadata[0].name
    labels    = local.labels
  }

  spec {
    type       = "ClusterIP"
    cluster_ip = "None"
    selector   = local.labels

    port {
      name        = "client"
      port        = 2379
      target_port = "client"
    }

    port {
      name        = "peer"
      port        = 2380
      target_port = "peer"
    }
  }
}

resource "kubernetes_storage_class" "etcd" {
  metadata {
    name   = "${local.release}-storageclass-ssd"
    labels = local.labels
  }

  storage_provisioner = "kubernetes.io/gce-pd"
  parameters = {
    type = "pd-ssd"
  }
}
