# Profile

The profile session will execute queries based on the list of profiles defined in your local configuration.

## Usage

```python
from cmq.aws.session import profile

# List all profiles starting with "test"
profile(name="test").list()

# List RDS resources in all profiles
profile().rds().list()
```

## Profile
::: cmq.aws.session.profile.profile

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource
