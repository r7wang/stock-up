provider "google" {
  version = "3.5.0"

  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

module "stock-analyzer" {
  vm_depends_on = [module.stock-config, module.stock-kafka]
  source  = "./gce-container"

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
      name = "KAFKA_TOPIC"
      value = "stock-quotes"
    }
  ]
}

module "stock-query" {
  vm_depends_on = [module.stock-config, module.stock-kafka]
  source  = "./gce-container"

  name = "stock-query"
  image = "gcr.io/${var.project}/stock-query:0.1"
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
      name = "KAFKA_TOPIC"
      value = "stock-quotes"
    }
  ]
}

module "stock-config" {
  source  = "./gce-container"

  name = "stock-config"
  image = "gcr.io/${var.project}/etcd/3.4.7"
  env = [
    {
      name = "ALLOW_NONE_AUTHENTICATION"
      value = "yes"
    }
  ]
}

module "stock-kafka" {
  vm_depends_on = [module.stock-zookeeper]
  source  = "./gce-container"

  name = "stock-kafka"
  image = "gcr.io/${var.project}/kafka:2.5.0"
  env = [
    {
      name = "KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE"
      value = "true"
    },
    {
      name = "KAFKA_CFG_ZOOKEEPER_CONNECT"
      value = "stock-zookeeper:2181"
    },
    {
      name = "ALLOW_PLAINTEXT_LISTENER"
      value = "yes"
    },
    {
      name = "KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP"
      value = "PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT"
    },
    {
      name = "KAFKA_CFG_LISTENERS"
      value = "PLAINTEXT://:9092,PLAINTEXT_HOST://:29092"
    },
    {
      name = "KAFKA_CFG_ADVERTISED_LISTENERS"
      value = "PLAINTEXT://stock-kafka:9092,PLAINTEXT_HOST://localhost:29092"
    }
  ]
}

module "stock-zookeeper" {
  source  = "./gce-container"

  name = "stock-zookeeper"
  image = "gcr.io/${var.project}/zookeeper/3.6.1"
  env = [
    {
      name = "ALLOW_ANONYMOUS_LOGIN"
      value = "yes"
    }
  ]
}