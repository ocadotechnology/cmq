# Region

List regions in the AWS account.

## Usage

```python
from cmq.aws.session import profile

# List all regions available in the AWS account
profile().region().list()
```

## Region
::: cmq.aws.resource.region.region

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource