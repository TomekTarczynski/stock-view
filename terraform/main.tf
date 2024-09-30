variable "docker_sha" {
  type = string
  default = "latest"  # Fallback value in case SHA is not provided
}

# Set the provider to AWS and region to eu-west-1
provider "aws" {
  region = "eu-west-1"
}

resource "aws_security_group" "allow_http_ssh" {
  name_prefix  = "allow_http_ssh_"  # Automatically adds a unique identifier
  description  = "Allow SSH and HTTP inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_http_ssh"
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
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl apt-transport-https software-properties-common
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add Docker's official repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu noble stable" | sudo tee /etc/apt/sources.list.d/docker.list

    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo systemctl start docker

    # Run your Docker container
    sudo docker run -d -p 80:8000 tomektarczynski/stock-view-backend:${docker_sha}
  EOF


  tags = {
    Name = "example-instance"
  }
}

# Output the public IP of the EC2 instance
output "instance_public_ip" {
  value = aws_instance.example.public_ip
}
