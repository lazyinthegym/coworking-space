## Push docker image to AWS ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 992382364567.dkr.ecr.us-east-1.amazonaws.com

docker build -t udacity-coworking-checkin .

docker tag udacity-coworking-checkin:latest 992382364567.dkr.ecr.us-east-1.amazonaws.com/udacity-coworking-checkin:latest

docker push 992382364567.dkr.ecr.us-east-1.amazonaws.com/udacity-coworking-checkin:latest
```


### Project Coworking Space

Creating the K8s cluster
```bash
# Create a cluster
eksctl create cluster --name coworking-space --region us-east-1 --nodegroup-name my-nodes --node-type t3.small --nodes 1 --nodes-min 1 --nodes-max 2

# Updates the kubeconfig file to use the specified EKS cluster, to be able to use kubectl
# The kubeconfig file is a configuration file used by `kubectl`, the command-line tool for interacting with Kubernetes clusters. It contains information such as the cluster's API # server address, authentication credentials, and context settings, enabling kubectl to manage and deploy applications on the specified Kubernetes cluster. 
# typically located at ~/.kube/config
aws eks --region us-east-1 update-kubeconfig --name coworking-space

# verify and copy the context name
kubectl config current-context

# delete the cluster
eksctl delete cluster --name coworking-space --region us-east-1
```

Configuring the Postgres service in the K8s cluster.
```bash
# ensure you are connected to your K8s cluster
kubectl get namespace

# Apply YAML configurations
kubectl apply -f pvc.yaml
kubectl apply -f pv.yaml
kubectl apply -f postgresql-deployment.yaml

# view the pods
kubectl get pods

# get the name of the pod, and open bash into the pod
kubectl exec -it postgresql-59657bc885-jnzw6 -- bash

# connect to the postgres database
psql -U ahmad -d mydatabase

# Once you are inside the postgres database, you can list all databases
\l

# Creeate the postgres service to expose the database to the outside world.
kubectl apply -f postgresql-service.yaml

# List the services
kubectl get svc

# Set up port-forwarding to `postgresql-service`
kubectl port-forward service/postgresql-service 5433:5432 &
```
