resource "aws_subnet" "east_2a" {
  vpc_id            = aws_vpc.stock.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = "us-east-2a"

  map_public_ip_on_launch = false

  tags = {
    Name = "subnet-stock-east-2a"
  }
}

resource "aws_subnet" "east_2b" {
  vpc_id            = aws_vpc.stock.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-2b"

  map_public_ip_on_launch = false

  tags = {
    Name = "subnet-stock-east-2b"
  }
}

resource "aws_subnet" "east_2c" {
  vpc_id            = aws_vpc.stock.id
  cidr_block        = "10.0.8.0/24"
  availability_zone = "us-east-2c"

  map_public_ip_on_launch = false

  tags = {
    Name = "subnet-stock-east-2c"
  }
}

resource "aws_subnet" "public_east_2a" {
  vpc_id            = aws_vpc.stock.id
  cidr_block        = "10.0.10.0/24"
  availability_zone = "us-east-2a"

  map_public_ip_on_launch = true

  tags = {
    Name = "subnet-stock-public-east-2a"
  }
}

resource "aws_subnet" "public_east_2b" {
  vpc_id            = aws_vpc.stock.id
  cidr_block        = "10.0.12.0/24"
  availability_zone = "us-east-2b"

  map_public_ip_on_launch = true

  tags = {
    Name = "subnet-stock-public-east-2b"
  }
}
