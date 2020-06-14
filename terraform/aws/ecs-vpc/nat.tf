resource "aws_eip" "default" {
  vpc = true
}

resource "aws_nat_gateway" "default" {
  allocation_id = aws_eip.default.id
  subnet_id     = aws_subnet.public_east_2b.id
}
