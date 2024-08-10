FROM python:slim

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
    jq \
    build-essential \
    libpq-dev \
    postgresql-client \
    netcat-openbsd

# Set environment variables
ENV DB_USERNAME=ahmad \
    DB_PASSWORD=dummypassword \
    DB_HOST=127.0.0.1 \
    DB_PORT=5433 \
    DB_NAME=mydatabase

# Set the working directory
WORKDIR /app

# Copy files into the container
COPY . .

# Install the required packages
RUN pip install -r requirements.txt

# Run the app (typically CMD or ENTRYPOINT should be used for running apps, not RUN)
CMD ["python", "app.py"]
