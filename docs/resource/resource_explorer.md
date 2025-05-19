# Resource Explorer

The Resource Explorer resource provides access to AWS Resource Explorer resources.

## Usage

```python
from cmq.aws.session import profile

# List all Resource Explorer resources
profile().resource_explorer().list()
```

## Resource Explorer
::: cmq.aws.resource.resource_explorer.resource_explorer

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource