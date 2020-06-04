locals {
  namespace = kubernetes_namespace.prod.metadata[0].name
}

provider "kubernetes" {
  config_context = "stock"
}

resource "kubernetes_namespace" "prod" {
  metadata {
    name = "prod"
  }
}

module "stock_analyzer" {
  source = "./stateless-service"

  namespace = local.namespace
  release   = "stock-analyzer"
  image     = "gcr.io/${var.project}/stock-analyzer:0.1"
  env = [
    {
      name  = "CONFIG_HOST"
      value = "${module.stock_config.service_name}.${local.namespace}.svc.cluster.local"
    },
    {
      name  = "MESSAGE_QUEUE_TYPE"
      value = "kafka"
    },
    {
      name  = "KAFKA_BROKERS"
      value = "${module.stock_kafka.service_name}.${local.namespace}.svc.cluster.local:${local.kafka_port}"
    },
    {
      name  = "KAFKA_TOPIC"
      value = "stock-quotes"
    },
    {
      name  = "INFLUXDB_HOST"
      value = "${module.stock_influxdb.service_name}.${local.namespace}.svc.cluster.local"
    },
    {
      name  = "INFLUXDB_PORT"
      value = local.influxdb_port
    },
    {
      name  = "INFLUXDB_USER"
      value = "admin"
    },
    {
      name  = "INFLUXDB_PASSWORD"
      value = var.influxdb_password
    },
    {
      name  = "INFLUXDB_DB_NAME"
      value = "stock"
    }
  ]
}

module "stock_query" {
  source = "./stateless-service"

  namespace = local.namespace
  release = "stock-query"
  image = "gcr.io/${var.project}/stock-query:0.1"
  env = [
    {
      name  = "CONFIG_HOST"
      value = "${module.stock_config.service_name}.${local.namespace}.svc.cluster.local"
    },
    {
      name  = "MESSAGE_QUEUE_TYPE"
      value = "kafka"
    },
    {
      name  = "KAFKA_BROKERS"
      value = "${module.stock_kafka.service_name}.${local.namespace}.svc.cluster.local:${local.kafka_port}"
    },
    {
      name  = "KAFKA_TOPIC"
      value = "stock-quotes"
    },
    {
      name  = "QUOTE_SERVER"
      value = "ws.finnhub.io"
    },
    {
      name  = "QUOTE_API_TOKEN"
      value = var.quote_api_token
    }
  ]
}
