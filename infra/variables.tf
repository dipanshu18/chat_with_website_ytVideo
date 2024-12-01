variable "ecr_image_uri" {
  default = "782266695170.dkr.ecr.us-east-1.amazonaws.com/chatapp:latest"
  description = "URI of the ECR image for the Lambda function"
  type        = string
}
