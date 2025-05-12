# Route53

The Route53 resource provides access to AWS Route53 DNS services.

## Usage

```python
from cmq.aws.session import profile

# List all hosted zones
profile().route53().list()

# Add describe operation to the resource 
profile().route53().describe().list()

# Add tags to the resource
profile().route53().tags().list()
```

## Route53
::: cmq.aws.resource.route53.route53

## Inherited from AWSResource
::: cmq.aws.aws.AWSResource
