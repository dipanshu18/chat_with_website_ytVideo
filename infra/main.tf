
data "aws_security_group" "wizard_1" {
  filter {
    name   = "group-name"
    values = ["launch-wizard-1"]
  }
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_instance" "chatapp_instance" {
  # for_each      = toset(data.aws_subnets.default.ids)
  ami           = "ami-0866a3c8686eaeeba" # Amazon Linux 2 AMI
  instance_type = "t2.xlarge"

  security_groups = [data.aws_security_group.wizard_1.id]
  subnet_id     = "subnet-0e409c4ba2f2ca479"

  root_block_device {
    volume_size = 30
    volume_type = "gp2"
  }
  key_name = "chatapp"

  tags = {
    Name = "ChatAppServer"
  }
  provisioner "remote-exec" {
    
    inline = [
    "sudo apt update && sudo apt upgrade -y",
    "sudo snap install docker",
    "sudo chmod 666 /var/run/docker.sock",
    "sudo snap install aws-cli --classic",
    "aws configure set aws_access_key_id ${var.aws_access_key}",
    "aws configure set aws_secret_access_key ${var.aws_secret_key}",
    "aws configure set default.region us-east-1",
    "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 782266695170.dkr.ecr.us-east-1.amazonaws.com/chatapp",
    "docker pull 782266695170.dkr.ecr.us-east-1.amazonaws.com/chatapp",
    "docker run -dit -p 8501:8501 --name chatapp 782266695170.dkr.ecr.us-east-1.amazonaws.com/chatapp"
    ]
    
    connection {
    type = "ssh"
    user = "ubuntu"
    private_key = file("/home/dipanshu/Downloads/chatapp.pem")
    host = self.public_ip
    
  }
}
}

output "public_ip" {
  value = aws_instance.chatapp_instance.public_ip
}
