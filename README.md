# Coworking Space Project

This project consists of a microservice application with two main services: a PostgreSQL database and an analytics application built using Flask and SQLAlchemy. The application is containerized using Docker, and the deployment is managed using Kubernetes (EKS on AWS). The app docker image build process is automated with AWS CodeBuild, and the Docker images are stored in AWS ECR.

## Table of Contents
1. [Technologies Used](#technologies-used)
2. [Deployment Process](#deployment-process)
   - [Build and Push Docker Image](#build-and-push-docker-image)
   - [Kubernetes Cluster Setup](#kubernetes-cluster-setup)
   - [Database Deployment](#database-deployment)
   - [Running SQL Scripts](#running-sql-scripts)
   - [Deploying the Analytics Application](#deploying-the-analytics-application)
   - [Monitoring with CloudWatch](#monitoring-with-cloudwatch)
3. [Releasing New Builds](#releasing-new-builds)

## Deployment Overview

### Technologies Used
- **Docker**: For containerizing the analytics application.
- **AWS CodeBuild**: Automates the building and pushing of Docker images to AWS ECR.
- **Kubernetes (EKS)**: Manages the deployment of services, providing scalability and resilience.
- **PostgreSQL**: Serves as the database backend for the application.
- **AWS CloudWatch**: Monitors logs and metrics for the deployed services.

### Deployment Process
1. **Build and Push Docker Image**:
   - Use AWS CodeBuild to automate the build of the Docker image with every push in this repo. The image is then pushed to AWS ECR for version control and easy retrieval during deployments.
  
2. **Kubernetes Cluster Setup**:
   - The application is deployed to an EKS cluster. The cluster can be created using `eksctl`, which simplifies the configuration and management of Kubernetes clusters on AWS.

3. **Database Deployment**:
   - The PostgreSQL database is deployed as a Kubernetes service. Persistent volumes, configurations, and secrets are managed through Kubernetes manifests.

4. **Deploying the Analytics Application**:
   - The Flask-based analytics application is deployed using a Kubernetes deployment manifest. Once deployed, it is exposed through a load balancer.

5. **Monitoring with CloudWatch**:
   - CloudWatch is configured to monitor the EKS cluster and application logs, providing insights into the system’s performance and potential issues.

### Releasing New App Builds
To release new builds:
1. Update the codebase and push changes to the repository. AWS CodeBuild will automatically build a new app docker image and push it to AWS ECR.
3. Update the deployment manifest (`app-deployment.yml`) with the new image link from ECR.
4. Redeploy the updated application using `kubectl apply -f app-deployment.yml`.