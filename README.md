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


## Pricing
The _minimum_ price for this server setup is in the ballpark of $35/mo (although, by disabling some options, $7/mo is possible). For small websites (<100,000 requests a day), it will likely not exceed $60/mo. You can more accurately gauge the price using the [AWS Pricing Calculator](https://calculator.aws/) (it's not "easy" to use, which is why I include the aforementioned estimate).

Every resource we create in this guide will have a link to detailed pricing information (TODO: actually do this), but here's a quick, rough breakdown:
TODO: format this better
```
ECR:
	storage:
		- $0.10 per GB / month

	estimate:
		- 10 GB = $1.00 / month
ECS:
	vCPU:
		- $0.04048 / vCPU / hour
	memory:
		- $0.004445 / GB / hour
	ip:
		- $0.005 / task / hour

	estimate:
		- 1 task, 0.25 vCPU, 0.5 GB = $12.49 / month
RDS:
	db.t4g.micro instance:
		- $0.016 / hour
	ip:
		- $0.005 / hour

	estimate:
		- $15.12 / month
ELB:
	flat rate:
		- $0.0225 / hour
	LCUs:
		- $0.008 / lcu / hour

	estimate:
		- 0.25 LCU = $17.64 / month
```

> [!IMPORTANT]  
> AWS will happily bill you for thousands of dollars if you accidentally scale up your server (or get attacked without autoscaling limits). Be careful, check your bill frequently and make sure you have reasonable scaling limits (covered in this guide)!

## AWS Setup Instructions
See [INSTRUCTIONS.md](./INSTRUCTIONS.md).

Estimated time:
- to blindly follow instructions without learning anything: **1 hour**
- surface level understanding of how services interconnect: **3 hours**
- in-depth understanding: **8 hours** (or more - the AWS hole goes **DEEP**)
- how long it took me, without an up-to-date guide: 16-20 hours (plus some time to document the process here)

## Local Setup
1. Install Docker 
2. Run `docker compose up --build`
3. Visit http://localhost/
