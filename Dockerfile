FROM ubuntu:latest

# Update the package lists
RUN apt-get update

# Install any necessary packages
RUN apt-get install -y \
    python3 \
    python3-pip \
    git \
    vim \
    curl \
    wget \
    unzip \
    jq

# Set the working directory
WORKDIR /app

# Copy files into the container
COPY . .

# Specify the command to run when the container starts
CMD ["/bin/bash"]