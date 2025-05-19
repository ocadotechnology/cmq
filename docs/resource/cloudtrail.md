# CloudTrail

The CloudTrail resource provides access to AWS CloudTrail trails.

## Usage

```python
from cmq.aws.session import profile

# List all CloudTrail trails
profile().cloudtrail().list()
```

## CloudTrail
::: cmq.aws.resource.cloudtrail.cloudtrail

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource