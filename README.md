## Push docker image to AWS ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 992382364567.dkr.ecr.us-east-1.amazonaws.com

docker build -t udacity-coworking-checkin .

docker tag udacity-coworking-checkin:latest 992382364567.dkr.ecr.us-east-1.amazonaws.com/udacity-coworking-checkin:latest

docker push 992382364567.dkr.ecr.us-east-1.amazonaws.com/udacity-coworking-checkin:latest
```