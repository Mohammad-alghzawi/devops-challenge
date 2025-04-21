#!/bin/bash

set -e

echo "Updating system"
sudo apt update && sudo apt upgrade -y

echo "Installing Git"
sudo apt install git -y

echo "Installing Docker"
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

echo "Installing Docker Compose"
sudo apt install docker-compose -y

echo "Adding user to docker group"
sudo usermod -aG docker $USER

echo "Cloning repository"
 git clone https://github.com/Mohammad-alghzawi/devops-challenge.git
 cd devops-challenge

echo "Starting Docker containers"
sudo docker-compose up -d


