resource "aws_vpc" "stock" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "vpc-stock"
  }
}

resource "aws_subnet" "east_2a" {
  vpc_id            = aws_vpc.stock.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = "us-east-2a"

  tags = {
    Name = "subnet-stock-east-2a"
  }
}

resource "aws_subnet" "east_2b" {
  vpc_id            = aws_vpc.stock.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-2b"

  tags = {
    Name = "subnet-stock-east-2b"
  }
}

resource "aws_subnet" "east_2c" {
  vpc_id            = aws_vpc.stock.id
  cidr_block        = "10.0.8.0/24"
  availability_zone = "us-east-2c"

  tags = {
    Name = "subnet-stock-east-2c"
  }
}

resource "aws_route_table" "stock" {
  vpc_id = aws_vpc.stock.id

  tags = {
    Name = "rt-stock"
  }
}

resource "aws_main_route_table_association" "stock" {
  vpc_id         = aws_vpc.stock.id
  route_table_id = aws_route_table.stock.id
}

resource "aws_internet_gateway" "stock" {
  vpc_id = aws_vpc.stock.id

  tags = {
    Name = "ig-stock"
  }
}
