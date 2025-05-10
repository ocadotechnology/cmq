# VPC

The VPC resource provides access to AWS Virtual Private Cloud resources.

## Usage

```python
from cmq.aws.session import profile

# List all VPCs
profile().vpc().list()

# Include describe to the resource
profile().vpc().describe().list()
```
    
## VPC
::: cmq.aws.resource.vpc.vpc

## Inherited from AWSResource
::: cmq.aws.aws.AWSResource
