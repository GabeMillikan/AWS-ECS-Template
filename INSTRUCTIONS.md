todo: screenshots + RDS + SSH + autoscaling + repo


1. Create IAM user for github-actions
    - name: "github-actions"
    - don't give console access
    - add permissions manually
    - add AmazonEC2ContainerRegistryFullAccess
2. Give GitHub access to this user
    - create access key for the user
    - select 'third party service' and ignore warning - create anyway (just cuz I don't wanna deal with more complicated options yet)
    - description: Used by GitHub Actions to push images during CI.
    - repository -> settings -> Secrets and variables -> Actions -> create secrets
        - AWS_ECR_SECRET_ACCESS_KEY: copy/paste the "secret access key" from aws
        - AWS_ECR_ACCESS_KEY_ID: copy/paste the "access key" from aws
3. Create a (private) ECR repository on AWS for each of the images that you want to launch in ECS
    - name: "fastapi"
4. Create or update a GitHub Actions workflow to build your images and push them to ECR.
    - see example: [build.yml](.github/workflows/build.yml)
5. Push some code and verify that the build and push succeeds. Check that a new `latest` image is available in the AWS console.
6. Create a Fargate cluster in ECS
    - name: "production-cluster"
7. Create IAM role `ecsTaskExecutionRole`
    - [guide in docs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html>
    - IAM -> Create Role
        - entity type: AWS service
        - service or use case: Elastic Container Service
        - use case: Elastic Container Service Task
        - add permission "AmazonECSTaskExecutionRolePolicy"
        - role name: "ecsTaskExecutionRole"
8. Create task definition
    - name: "production-task-definition"
    - launch type: fargate
    - os: linux/x64
    - task size: .25 vcpu, .5 gb memory
    - task role: none
    - task execution role: ecsTaskExecutionRole
    - container 1
        - name: "fastapi"
        - image uri: copy from ECR (make sure to copy the tag as well, like ...fastapi:latest, not just the repository)
        - port mappings: 8081 TCP (no name/protocol override)
        - default log collection enabled
9. Create VPC
    - VPCs -> Create VPC and more
    - auto-generated name scheme: "production" (so final vpc is named "production-vpc" and gateway is "production-igw" etc.)
    - ipv4 cidr: 10.0.0.0/16
    - no ipv6
    - 3 AZs
    - 3 public subnets
    - 0 private subnets
    - no NAT
    - no S3 endpoints
    - enable DNS hostnames + resolution
10. Create security group for load balancer
    - Security Group -> Create
    - name: "production-load-balancer-security-group"
    - description: allows inbound TCP traffic on ports 80 and 443
    - vpc: production-vpc
    - add inbound rules to allow TCP on port 80 + 443 for ipv4 + ipv6
    - remove any outbound rules (LB shouldn't be making requests TODO: healthcheck requests?)
11. Create security group for ecs service
    - Security Group -> Create
    - name: "production-ecs-service-security-group"
    - description: allows inbound traffic from load balancer
    - vpc: production-vpc
    - allow all tcp traffic from security group production-load-balancer-security-group
12. Create target group
    - name: "production-target-group"
    - target type: IP
    - protocol/port: HTTP/8081
    - vpc: production-vpc
    - protocol version: http/1.1 (note that http/2 requests can be translated within the load balancer)
    - leave health check at the root
    - remove any IP addresses
    - ensure port is still 8081
    - don't add any targets (we haven't created the cluster service yet)
13. Create load balancer
    - application load balancer
    - name: "production-load-balancer"
    - internet facing
    - ipv4
    - production-vpc
    - enable mappings for all AZs (public subnets)
    - listener for port 80 points to production-target-group (TODO: add listener for :443)
    - hit "create" and wait for "State" to be 'active'
14. Create ECS service
    - ECS -> clusters -> production-cluster -> services -> create
    - fargate capacity provider
    - application type: service
    - task family: production-task-definition (LATEST)
    - name: "production-service"
    - desired tasks: 2 (for now, just to test balancing - later setup autoscaling)
    - networking
        - vpc: production-vpc
        - subnets: public subnets
        - security group: production-ecs-service-security-group
        - auto-assign public IP: enabled (ALMOST CERTAINLY NOT REQUIRED: TODO)
    - load balancing
        - application load balancer
        - container: select fastapi 8081:8081 (TODO: TLS?)
        - use existing load balancer: production-load-balancer
        - use existing listener: 80:HTTP
        - use existing target group: production-target-group

## Table of Contents

- [Target Audience](#target-audience) (recommended level of experience)
- [Initialize GitHub Project](#initialize-git-hub-project) (setting up and building containers)
- [How This Repository Works](#how-this-repository-works) (overview of the layout of code)
- [Initialize AWS Project](#initialize-aws-project-create-a-vpc) (basic AWS configuration: create VPC + ECR repos)
- [Upload Images to ECR](#upload-images-to-ecr-via-git-hub-actions) (setup GitHub -> AWS pipeline)

## Target Audience
These instructions are detailed enough for beginners to understand them, but this is a complex project. It is unlikely that a beginner (to git, cloud hosting, or Docker) will learn anything substantial. I personally recommend accomplishing the following _before_ trying to follow this guide:
- Creating a GitHub repository with several branches and opening + merging some PRs.
- Creating and connecting to a virtual private server on any cloud platform (i.e. an EC2 instance).
- Building an executing a Docker container

If you're ambitious, I won't stop you, but be extremely careful about billing!



## Initialize GitHub Project
1. Create a GitHub account, and clone this repository.
2. todo

## How This Repository Works

todo: explain how the repo layout works

## Initialize AWS Project *(Create a VPC)*

1. Create an AWS account.
    - [direct link](https://portal.aws.amazon.com/billing/signup#/start/email)
    - **Highly Recommended**: use a debit card with a transaction limit. There is no limit to how much AWS might charge you if you're not careful. I've found success with [privacy.com](https://privacy.com/) (not affiliated, unless you want to use my [referral link](https://app.privacy.com/join/LURP8) for a $5 credit).
2. Login to AWS Console
    - [direct link](https://aws.amazon.com/console/) (you may have to click "log back in")
3. Choose a region
    - In the top right, click the dropdown next to your name. This is where your server will be physically located. I will choose us-east-2 simply because it is the cheapest location in the U.S. (by a small margin), but any other choice will suffice. This guide will only cover single-region setups (for now; I haven't explored multi-region deployments yet). 
    <details>
        <summary>See Image</summary>
        <img src="./.readme-images/select-region.png" width="350px"/>
    </details>
4. Use the search bar to find the VPC service
    - Stands for "Virtual Private Cloud"
    - We'll be using it to create a LAN network to contain all of our servers, the database, etc.
    <details>
        <summary>See Image</summary>
        <img src="./.readme-images/searchbar-vpc.png" height="150px"/>
    </details>
5. Go to "Your VPCs"
    <details>
        <summary>See Image</summary>
        <img src="./.readme-images/your-vpcs.png" width="150px"/>
    </details>
6. Click "Create VPC"
    - in the upper right
    - Note: this is the last time that I will explain UI navigation. It is quite consistent going forward.
    <details>
        <summary>See Image</summary>
        It's okay if you already have a VPC here, just create another one.
        <img src="./.readme-images/create-vpc.png" height="150px"/>
    </details>
7. Configure your VPC, then hit "Create VPC"
    - Select "Create VPC and More", since we want to configure subnets.
    - Give it an autogenerated, unique name. We will be naming _every_ AWS resource, so try to keep things consistent for your own sanity. I will use the name `template-guide` (i.e. so that the VPC is called `template-guide-vpc`).
    - Enable at least two Availability Zones (required for the Load Balancer). More is better, but may incur additional costs if you plan on transferring data between server instances (not including via the database). TODO: double check this information.
    - Create zero private subnets, we simply won't need them (as these are web-servers and need to be internet-connected).
    - Do not create any NAT gateways or S3 endpoints, they're pricy and we won't use them.
    <details>
        <summary>See Image</summary>
        <img src="./.readme-images/vpc-configuration.png"/>
    </details>
8. Create ECR Repositories
    - Go to ECR -> Private Registry -> Repositories
    - Create two repositories, one for the NGINX image and one for the FastAPI image.
    - I will create private repositories named `template-guide-nginx` and `template-guide-fastapi`, but you may choose to publish them (if you know what you're doing).
    <details>
        <summary>See Images</summary>
        <img src="./.readme-images/create-ecr-repo.png" height="600px"/>
        <img src="./.readme-images/created-ecr-repos.png"/>
    </details>

## Upload Images to ECR (via GitHub Actions)

1. Create an IAM User for GitHub Actions
    - Go to IAM -> Users -> Create User
    - I will name mine `template-guide-github-actions`
    - Do not provide console access (GitHub doesn't need it)
    - Attach policies directly, and select `AmazonEC2ContainerRegistryFullAccess` (to enable read and write access to your ECR repositories)
    <details>
        <summary>See Image</summary>
        <img src="./.readme-images/iam-gh-actions-review.png" width="600px"/>
    </details>
2. Create an Access Key for the IAM User
    - click into your newly created user
    - click "Create access key"
    - Select "Third-party service" as your use case (GitHub is a third-party)
    - Confirm that you understand creating permanent access keys is not good practice, and hit Next. Otherwise, please figure out how to use IAM Roles and open a PR to update this guide.
    - A good description is something like "Authorizes GitHub Actions for GabeMillikan/AWS-ECS-Template to upload ECR images.". Be specific to avoid confusion later.
    - > [!NOTE]
      > Do not navigate away from the page, you'll need it in step 4.
    - If you've ignored the above note, then delete the access key and start over.
    <details>
        <summary>See Image</summary>
        <img src="./.readme-images/iam-create-access-key.png" width="600px"/>
    </details>
3. Open Repository settings
    - Visit your repository on github.com
    - go to the "Settings" tab at the top (i.e. to the right of the Code/Issues/Pull Requests tabs)
    <details>
        <summary>See Image</summary>
        <img src="./.readme-images/github-repository-settings-tab.png" width="450px"/>
    </details>
4. (currently testing if I need to enable actions permissions or not)


TODO: copy/paste me for security groups
Create a Security Group for GitHub Actions
    - Which will give GitHub access to your private ECR repositories
    - Note: it doesn't matter if you get to "Security Groups" as an EC2 feature or as a VPC feature, they are the same (the search bar returns both, for some reason).
    - I will **name** mine `template-guide-github-actions-sg`
    - Give it a **description** along the lines of "Authorizes GitHub Actions for GabeMillikan/AWS-ECS-Template to upload ECR images and force new ECS deployments"
        - Being specific is useful, because we will create multiple security groups.
        - We won't actually allow GitHub to "force new ECS deployments" *yet* (that will come later), but you cannot change the description so we need to include this now (you're welcome, for telling you now).
    - Select the **VPC** you created earlier (mine is named `template-guide-vpc`)
    - 