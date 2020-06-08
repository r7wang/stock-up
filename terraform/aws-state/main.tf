provider "aws" {
  version = "~> 2.0"

  region  = "us-east-2"
  profile = "prod"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "stock-up-terraform-state"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "stock-up-terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
