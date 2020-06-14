resource "aws_vpc" "stock" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "vpc-stock"
  }
}

resource "aws_route_table" "stock" {
  vpc_id = aws_vpc.stock.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.default.id
  }

  tags = {
    Name = "rt-stock-private"
  }
}

resource "aws_main_route_table_association" "stock" {
  vpc_id         = aws_vpc.stock.id
  route_table_id = aws_route_table.stock.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.stock.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.stock.id
  }

  tags = {
    Name = "rt-stock-public"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public_east_2b.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "stock" {
  name   = "stock"
  vpc_id = aws_vpc.stock.id

  ingress {
    description = "Allow ingress from security group"

    protocol  = "-1"
    from_port = 0
    to_port   = 0
    self      = true
  }

  ingress {
    description = "Allow SSH access"

    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sg-stock"
  }
}

resource "aws_security_group" "efs" {
  name   = "efs"
  vpc_id = aws_vpc.stock.id

  ingress {
    description = "Allow NFS access"

    protocol        = "tcp"
    from_port       = 2049
    to_port         = 2049
    security_groups = [aws_security_group.stock.id]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sg-efs"
  }
}

resource "aws_internet_gateway" "stock" {
  vpc_id = aws_vpc.stock.id

  tags = {
    Name = "ig-stock"
  }
}
