this is nowhere near done yet - if you're reading this, check back in a year

> [!NOTE]
> If you have any experience with this, please open a PR and add your comments!

# What is this?
This repository is a fairly basic template & tutorial for deploying a production web server on [Amazon's ECS](https://aws.amazon.com/ecs/), with the following features:
- A decent local-development experience; entirely dockerized
- Automatic build + deployment on push to main branch
- RDS database
- Fargate + Load Balancing = horizontally scalable
- FastAPI + React used for demonstration (could easily be swapped out for any other stack)


I provide no guarantee regarding the quality of this guide, I am simply documenting my own learnings while approaching this kind of infrastructure for the first time.


### Pricing
The _minimum_ price for this server setup is in the ballpark of $35/mo (although, by disabling some options, $7/mo is possible). For small websites (<100,000 requests a day, it will likely not exceed $60/mo). You can more accurately gauge the price using the [AWS Pricing Calculator](https://calculator.aws/) (it's not "easy" to use, which is why I include the aforementioned estimate).

Every resource we create in this guide will have a link to detailed pricing information, but here's a quick, rough breakdown:
- **ECS**: $7/mo for the smallest task
- **EC2**: $16/mo for a load balancer (lower quality workaround: free)
- **RDS**: $10/mo for the smallest Postgres database (lower quality workaround: free)

> [!IMPORTANT]  
> AWS will happily bill you for thousands of dollars if you accidentally scale up your server (or get attacked without autoscaling limits). Be careful, check your bill frequently and make sure you have reasonable scaling limits (covered in this guide)!

### AWS Setup Instructions
See [AWS.md](./instructions/AWS.md)

### Repository Setup Instructions
See [REPOSITORY.md](./instructions/REPOSITORY.md)
