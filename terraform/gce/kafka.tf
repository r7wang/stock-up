module "stock_kafka" {
  vm_depends_on = [module.stock_zookeeper]
  source        = "./gce-container"

  name  = "stock-kafka"
  image = "gcr.io/${var.project}/kafka:2.5.0"
  env = [
    {
      name  = "KAFKA_CFG_ZOOKEEPER_CONNECT"
      value = "stock-zookeeper:2181"
    },
    {
      name  = "ALLOW_PLAINTEXT_LISTENER"
      value = "yes"
    },
    {
      name  = "KAFKA_CFG_LISTENERS"
      value = "PLAINTEXT://:9092"
    },
    {
      name  = "KAFKA_CFG_ADVERTISED_LISTENERS"
      value = "PLAINTEXT://stock-kafka:9092"
    }
  ]
}
