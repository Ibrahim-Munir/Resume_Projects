provider "aws" {
  region = "your-preferred-region"
}

# Creating a VPC
resource "aws_vpc" "honey_pot_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "HoneyPotVPC"
  }
}

# Creating a subnet within the VPC
resource "aws_subnet" "honey_pot_subnet" {
  vpc_id     = aws_vpc.honey_pot_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "your-preferred-availability-zone"
  tags = {
    Name = "HoneyPotSubnet"
  }
}

# Creating an S3 Bucket as a decoy resource
resource "aws_s3_bucket" "decoy_bucket" {
  bucket = "decoy-bucket-name"
  acl    = "private"
}

# Creating a DynamoDB Table as a decoy resource
resource "aws_dynamodb_table" "decoy_table" {
  name           = "decoy-table-name"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"
  attribute {
    name = "id"
    type = "S"
  }
}

# Enabling CloudTrail for logging
resource "aws_cloudtrail" "honey_pot_trail" {
  name                          = "HoneyPotTrail"
  s3_bucket_name                = aws_s3_bucket.decoy_bucket.id
  enable_log_file_validation    = true
}

# Creating an SNS topic for email notifications
resource "aws_sns_topic" "honey_pot_notifications" {
  name = "HoneyPotNotifications"
}

# Subscribing an email endpoint to the SNS topic
resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.honey_pot_notifications.arn
  protocol  = "email"
  endpoint  = "your-email@example.com"
}

# Remember to replace placeholders like your-preferred-region, your-preferred-availability-zone, decoy-bucket-name, decoy-table-name, and your-email@example.com with your specific configurations.

This Terraform script sets up the VPC, subnet, S3 bucket, DynamoDB table, CloudTrail for logging, and SNS topic for email notifications, giving you a basic Honey Pot architecture in AWS.
