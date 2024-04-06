this is nowhere near done yet - if you're reading this, check back in a year


# What is this?
This repository is a fairly basic template & tutorial for deploying a production web server on [Amazon's ECS](https://aws.amazon.com/ecs/), with the following features:
- A decent local-development experience; entirely dockerized
- Automatic build + deployment on push to main branch
- RDS database
- Fargate + Load Balancing = horizontally scalable
- FastAPI + React used for demonstration (could easily be swapped out for any other stack)


I provide no guarantee regarding the quality of this guide, I am simply documenting my own learnings while approaching this kind of infrastructure for the first time.

> [!NOTE]  
> If you have any improvements, please open a PR!

> [!IMPORTANT]  
> The minimum price for this server setup is about $30/mo, assuming the server is online 24/7. If you accidentally scale up your server, it may cost you thousands. Be careful, check your bill frequently!

### AWS Setup Instructions
See [AWS.md](./instructions/AWS.md)

### Repository Setup Instructions
See [REPOSITORY.md](./instructions/REPOSITORY.md)
