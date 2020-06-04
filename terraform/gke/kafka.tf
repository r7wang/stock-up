locals {
  kafka_port = 9092
}

module "stock_kafka" {
  source = "./stateful-service"

  namespace  = local.namespace
  release    = "stock-kafka"
  image      = "gcr.io/${var.project}/kafka:2.5.0"
  mount_path = "/bitnami"

  ports = [
    {
      name = "client"
      port = local.kafka_port
    }
  ]

  env = [
    {
      name  = "KAFKA_CFG_ZOOKEEPER_CONNECT"
      value = "${module.stock_zookeeper.service_name}.${local.namespace}.svc.cluster.local:${local.zookeeper_port}"
    },
    {
      name  = "ALLOW_PLAINTEXT_LISTENER"
      value = "yes"
    },
    {
      name  = "KAFKA_CFG_LISTENERS"
      value = "PLAINTEXT://:${local.kafka_port}"
    },
    {
      name  = "KAFKA_CFG_ADVERTISED_LISTENERS"
      value = "PLAINTEXT://${module.stock_kafka.service_name}.${local.namespace}.svc.cluster.local:${local.kafka_port}"
    }
  ]
}
