resource "aws_service_discovery_private_dns_namespace" "stock" {
  name = "stock.app"
  vpc  = aws_vpc.stock.id
}
