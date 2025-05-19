# Keyspace Table

The Keyspace Table resource provides access to AWS Keyspaces tables.

## Usage

```python
from cmq.aws.session import profile

# List all Keyspaces tables
profile().keyspace_table().list()
```

## Keyspace Table
::: cmq.aws.resource.keyspace_table.keyspace_table

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource