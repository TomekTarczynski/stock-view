# Set the provider to AWS and region to eu-west-1
provider "aws" {
  region = "eu-west-1"
}

# Create a security group to allow SSH and HTTP access
resource "aws_security_group" "allow_http_ssh" {
  name        = "allow_http_ssh"
  description = "Allow SSH and HTTP inbound traffic"

  # Allow SSH from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTP from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an EC2 instance
resource "aws_instance" "example" {
  ami           = "ami-03cc8375791cb8bcf"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  key_name      = "tt_key"  # Your existing AWS key pair

  # Attach the security group
  vpc_security_group_ids = [aws_security_group.allow_http_ssh.id]

  # User data to install Docker and start the FastAPI app (optional)
  user_data = <<-EOF
              #!/bin/bash
              sudo amazon-linux-extras install docker -y
              sudo service docker start
              sudo usermod -a -G docker ec2-user
              sudo docker run -d -p 80:8000 your-dockerhub-username/stock-view-backend:latest
              EOF

  tags = {
    Name = "example-instance"
  }
}

# Output the public IP of the EC2 instance
output "instance_public_ip" {
  value = aws_instance.example.public_ip
}
