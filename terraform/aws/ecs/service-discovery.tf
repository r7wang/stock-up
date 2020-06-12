resource "aws_service_discovery_private_dns_namespace" "stock" {
  name = "stock.app"
  vpc  = data.aws_vpc.stock.id
}
