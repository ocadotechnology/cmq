# User Key

The User Key resource provides access to AWS IAM user keys.

## Usage

```python
from cmq.aws.session import profile

# List all user keys
profile().user_key().list()
```

## User Key
::: cmq.aws.resource.user_key.user_key

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource