# Coworking Space Project
- This is a microservice application that has 2 distinct services: database service, and an analytics application service
- Set up CodeBuild project to build the docker image and pushes it to AWS ECR.
- Create a EKS (K8s) cluster using `eksctl`
- Connect to the cluster using `kubectl`. You will use `kubectl` from now on to interact with the cluster.

# Project Structure
- `postgresql-deployment.yaml` & `postgresql-service.yaml`: Kubernetes configuration files for deploying the Postgres database and its service.

- `pvc.yaml` & `pv.yaml`: Kubernetes configuration files for creating a Persistent Volume Claim (PVC) and a Persistent Volume (PV) for the Postgres database.

- directory `db`: Contains the SQL scripts to create the database schema and seed the database with data.

- directory `analytics`: TODO


# Concepts and Notes:
## Kubectl 
- The `kubectl` tool is a command-line interface for interacting with Kubernetes clusters.
- it needs to connect to the cluster first to be able to use `kubectl` commands.
- The `kubectl` tool uses the `kubeconfig` file to connect to the cluster, which is typically located at `~/.kube/config`.

## Kubernetes (K8s)
- **Pods** are the smallest deployable units that can be created, managed, and scaled. A pod typically encapsulates one or more containers (usually Docker containers), along with their shared storage, network, and specifications on how to run them.

- **Services** are abstractions that define a logical set of Pods and a policy to access them. Services enable network access to Pods, providing stable IP addresses and DNS names even as the underlying Pods are created and destroyed.

- **Cluster** is a set of nodes (machines) that run containerized applications managed by Kubernetes. It includes a master node (control plane) that manages the cluster and worker nodes that run the containers. The cluster coordinates the scheduling, scaling, and management of all Pods and Services across the nodes.

## Instructions: How to deploy the project

### Step 1: Set up the CodeBuild project
This is done on the AWS console. We will create a CodeBuild project that will link to this repo to build the docker image and push it to AWS ECR.

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
Configuring the Postgres service in the K8s cluster.
```bash
# ensure you are connected to your K8s cluster
kubectl get namespace

# Apply YAML configurations
kubectl apply -f pvc.yaml
kubectl apply -f pv.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f postgresql-deployment.yaml
kubectl apply -f postgresql-service.yaml
kubectl apply -f app-deploy.yml

# View the pods to verify a pod is running
kubectl get pods

# Creeate the postgres service to expose the database to the outside world.
kubectl apply -f postgresql-service.yaml

# List the services to verify the service is running
kubectl get services

# Set up port-forwarding to `postgresql-service`
kubectl port-forward service/postgresql-service 5433:5432 &
```

### Step 4: Run the SQL scripts to create the database schema and seed the database with data

- Connect the database. 
The following will opens up port forwarding from your local environment's port 5433 to the node's port 5432. The `&` at the end ensures the process runs in the background.
```bash
# List the services to make sure the postgres service is running
kubectl get services

# Set up port-forwarding to `postgresql-service`
kubectl port-forward service/postgresql-service 5433:5432 &
```

- Run the SQL scripts to create the database schema and seed the database with data.
```bash
# The user-name, password and database name are the same as defined in the `postgresql-deployment.yaml` file
cd db
export DB_PASSWORD=dummypassword
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U ahmad -d mydatabase -p 5433 < 1_create_tables.sql
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U ahmad -d mydatabase -p 5433 < 2_seed_users.sql
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U ahmad -d mydatabase -p 5433 < 3_seed_tokens.sql
```

- Verify the database is created and seeded with data.
```bash
# open a psql shell to the database
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U ahmad -d mydatabase -p 5433

# List the tables
\dt

# Query the users table
SELECT * FROM users;

# Close the psql shell
\q
```

### Step 5: Deploy the analytics application
TODO

### Step 6: Clean up
- Delete the K8s cluster
```bash
eksctl delete cluster --name coworking-space --region us-east-1
```

- Cancel the port-forwarding
```bash
ps aux | grep 'kubectl port-forward' | grep -v grep | awk '{print $2}' | xargs -r kill
```
