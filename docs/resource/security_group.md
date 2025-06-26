# Security Groups

The Security Groups resource provides access to AWS EC2 Security Groups.

## Usage

```python
from cmq.aws.session import profile

# List all Security Groups
profile().security_group().list()
```

## Inherited from Security Groups
::: cmq.aws.resource.security_group.security_group

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource