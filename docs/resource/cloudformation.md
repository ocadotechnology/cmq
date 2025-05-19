# CloudFormation

The CloudFormation resource provides access to AWS CloudFormation stacks.

## Usage

```python
from cmq.aws.session import profile

# List all CloudFormation stacks
profile().cloudformation().list()
```

## CloudFormation
::: cmq.aws.resource.cloudformation.cloudformation

### Inherited from ResourceInterface
::: cmq.base.ResourceInterface
### Inherited from Resource
::: cmq.base.Resource