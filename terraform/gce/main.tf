provider "google" {
  version = "3.5.0"

  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

module "stock_analyzer" {
  vm_depends_on = [module.stock_config, module.stock_kafka, module.stock_influxdb]
  source        = "./gce-container"

  name  = "stock-analyzer"
  image = "gcr.io/${var.project}/stock-analyzer:0.1"
  env = [
    {
      name  = "CONFIG_HOST"
      value = "stock-config"
    },
    {
      name  = "MESSAGE_QUEUE_TYPE"
      value = "kafka"
    },
    {
      name  = "KAFKA_BROKERS"
      value = "stock-kafka:9092"
    },
    {
      name  = "KAFKA_TOPIC"
      value = "stock-quotes"
    },
    {
      name  = "INFLUXDB_HOST"
      value = "stock-influxdb"
    },
    {
      name  = "INFLUXDB_PORT"
      value = "8086"
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
  vm_depends_on = [module.stock_config, module.stock_kafka]
  source        = "./gce-container"

  name      = "stock-query"
  image     = "gcr.io/${var.project}/stock-query:0.1"
  disk_size = 15

  env = [
    {
      name  = "CONFIG_HOST"
      value = "stock-config"
    },
    {
      name  = "MESSAGE_QUEUE_TYPE"
      value = "kafka"
    },
    {
      name  = "KAFKA_BROKERS"
      value = "stock-kafka:9092"
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
