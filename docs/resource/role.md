# Role

The Role resource provides access to AWS IAM roles.

## Usage

```python
from cmq.aws.session import profile

# List all roles
profile().role().list()
```

## Role
::: cmq.aws.resource.role.role

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource