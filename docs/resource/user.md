# User

The User resource provides access to AWS IAM users.

## Usage

```python
from cmq.aws.session import profile

# List all users
profile().user().list()
```

## User
::: cmq.aws.resource.user.user

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource