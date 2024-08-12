# Coworking Space Project
- This is a microservice application that has 2 distinct services: database service, and an analytics application serviceclear

# Project Structure
- `postgresql-deployment.yaml` & `postgresql-service.yaml`: Kubernetes configuration files for deploying the Postgres database and its service.

- `pvc.yaml` & `pv.yaml`: Kubernetes configuration files for creating a Persistent Volume Claim (PVC) and a Persistent Volume (PV) for the Postgres database.

- directory `db`: Contains the SQL scripts to create the database schema and seed the database with data.

- directory `analytics`: The application code and the dockerfile of its environment.




# Instructions: How to deploy the project
### Step 1: Set up and run the CodeBuild project
This is done on the AWS console. Create a CodeBuild project that will link to this repo to build the docker image and push it to AWS ECR.

After the build succeeds, edit the following line in [app-deployment.yml](./app-deployment.yml#L33) and change the tag to the correct url of the docker image on the AWS docker hub. 

### Step 2: Create the K8s cluster
Create a K8s cluster with name `coworking-space`. You will connect `kubectl` tool to this cluster to interact with it.

```bash
# Create a cluster
eksctl create cluster --name coworking-space --region us-east-1 --nodegroup-name my-nodes --node-type t3.small --nodes 1 --nodes-min 1 --nodes-max 2

# Connect the local `kubectl` tool to the EKS cluster, to be able to interact with the cluster.
aws eks --region us-east-1 update-kubeconfig --name coworking-space

# verify the context name to make sure you are connected to the correct cluster
kubectl config current-context
```

### Step 3: Deploy the Postgres database and its service
```bash
# Apply YAML configurations
kubectl apply -f pvc.yaml
kubectl apply -f pv.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f postgresql-deployment.yaml
kubectl apply -f postgresql-service.yaml
```

### Step 4: Run the SQL scripts to create the database schema and seed the database with data 
The following will opens up port forwarding from your local environment's port 5432 to the node's port 5432. The `&` at the end ensures the process runs in the background. And then run the sql scripts
```bash
kubectl port-forward svc/postgresql-service 5432:5432 &

psql -h localhost -U ahmad -d users-database -f db/1_create_tables.sql
psql -h localhost -U ahmad -d users-database -f db/2_seed_users.sql
psql -h localhost -U ahmad -d users-database -f db/3_seed_tokens.sql
```

### Step 5: Deploy and test the analytics application
```bash
# deploy the app
kubectl apply -f app-deployment.yml

# Get the URL of the app
APP_EXTERNAL_IP=$(kubectl get services coworking -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test the app using curl commands
curl $APP_EXTERNAL_IP:5153/api/reports/daily_usage
curl $APP_EXTERNAL_IP:5153/api/reports/user_visits | jsonpp
```

### Step 6: Set up CloudWatch
```bash
aws iam attach-role-policy \
--role-name eksctl-coworking-space-nodegroup-m-NodeInstanceRole-ntmJOcKQpR2L \
--policy-arn arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy 

aws eks create-addon --addon-name amazon-cloudwatch-observability --cluster-name coworking-space --region us-east-1

```

### Clean up
- Delete the K8s cluster
```bash
eksctl delete cluster --name coworking-space --region us-east-1
```

- Cancel the port-forwarding
```bash
ps aux | grep 'kubectl port-forward' | grep -v grep | awk '{print $2}' | xargs -r kill
```

- Delete the docker image from AWS ECR using the the AWS console

# Concepts and Notes:
## Kubectl 
- The `kubectl` tool is a command-line interface for interacting with Kubernetes clusters.
- it needs to connect to the cluster first to be able to use `kubectl` commands.
- The `kubectl` tool uses the `kubeconfig` file to connect to the cluster, which is typically located at `~/.kube/config`.

## Kubernetes (K8s)
- **Pods** are the smallest deployable units that can be created, managed, and scaled. A pod typically encapsulates one or more containers (usually Docker containers), along with their shared storage, network, and specifications on how to run them.

- **Services** are abstractions that define a logical set of Pods and a policy to access them. Services enable network access to Pods, providing stable IP addresses and DNS names even as the underlying Pods are created and destroyed.

- **Cluster** is a set of nodes (machines) that run containerized applications managed by Kubernetes. It includes a master node (control plane) that manages the cluster and worker nodes that run the containers. The cluster coordinates the scheduling, scaling, and management of all Pods and Services across the nodes.