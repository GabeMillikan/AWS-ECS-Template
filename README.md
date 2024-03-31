this is nowhere near done yet - if you're reading this, check back in a year


# AWS ECS Notes
### Setup
1. Create an AWS account
2. Search for ECS (Elastic Container Storage) and select Ohio as the region (it's the cheapest). Direct link [here](https://us-east-2.console.aws.amazon.com/ecs/v2/clusters?region=us-east-2).
3. Click "Create Cluster" and under "Infrastructure" enable Fargate to simplify the server configuration. It will scale the container automatically. Enter a name and hit "Create".
4. Go to "Task Definitions" on the left navbar and click "Create New ..."
5. Give it a family name and select Fargate as the launch type.