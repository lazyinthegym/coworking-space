# Coworking Space Project
This project is a microservice application consisting of two services: a PostgreSQL database service and an analytics application built with Flask and SQLAlchemy. 
The docker image for the application is built and published using AWS Codebuild, and the services are deployed using Kubernetes. 

---

## Instructions: How to Deploy the Project

### Step 1: Set up and run the CodeBuild project
Create a CodeBuild project on the AWS console linked to this repo to build the Docker image and push it to AWS ECR. After the build succeeds, update the tag in [app-deployment.yml](./app-deployment.yml#L33) with the correct Docker image URL.

### Step 2: Create the K8s cluster
```bash
eksctl create cluster --name coworking-space --region us-east-1 --nodegroup-name my-nodes --node-type t3.small --nodes 1 --nodes-min 1 --nodes-max 2
aws eks --region us-east-1 update-kubeconfig --name coworking-space
kubectl config current-context
```

### Step 3: Deploy the Postgres database and its service
```bash
cd deployments
kubectl apply -f pvc.yaml -f pv.yaml -f configmap.yaml -f secret.yaml -f postgresql-deployment.yaml -f postgresql-service.yaml
```

### Step 4: Run the SQL scripts
```bash
kubectl port-forward svc/postgresql-service 5432:5432 &
psql -h localhost -U ahmad -d users-database -f db/1_create_tables.sql
psql -h localhost -U ahmad -d users-database -f db/2_seed_users.sql
psql -h localhost -U ahmad -d users-database -f db/3_seed_tokens.sql
```

### Step 5: Deploy and test the analytics application
```bash
kubectl apply -f app-deployment.yml
APP_EXTERNAL_IP=$(kubectl get services coworking -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl $APP_EXTERNAL_IP:5153/api/reports/daily_usage
curl $APP_EXTERNAL_IP:5153/api/reports/user_visits | jsonpp
```

### Step 6: Set up CloudWatch
```bash
aws iam attach-role-policy --role-name eksctl-coworking-space-nodegroup-m-NodeInstanceRole-ntmJOcKQpR2L --policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy 
aws eks create-addon --addon-name amazon-cloudwatch-observability --cluster-name coworking-space --region us-east-1
```

### Clean up
```bash
eksctl delete cluster --name coworking-space --region us-east-1
ps aux | grep 'kubectl port-forward' | grep -v grep | awk '{print $2}' | xargs -r kill
```

---