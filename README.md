this is nowhere near done yet - if you're reading this, check back in a year


# AWS Notes
### Github -> ECR setup
1. Create IAM user for github actions
    - iam -> users -> create user
        - example name: "github-actions"
        - Add permission "AmazonEC2ContainerRegistryFullAccess"
    - Create Access Key
    - copy the key id and secret into github repository -> settings -> secrets -> actions