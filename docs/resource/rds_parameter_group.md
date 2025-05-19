# RDS Parameter Groups

The RDS Parameter Groups resource provides access to AWS RDS parameter groups.

## Usage

```python
from cmq.aws.session import profile

# List all RDS parameter groups
profile().rds_parameter_group().list()
```

## RDS Parameter Groups
::: cmq.aws.resource.rds_parameter_group.rds_parameter_group

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource