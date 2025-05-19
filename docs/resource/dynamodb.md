# DynamoDB

The DynamoDB resource provides access to AWS DynamoDB tables.

## Usage

```python
from cmq.aws.session import profile

# List all DynamoDB tables
profile().dynamodb().list()
```

## DynamoDB
::: cmq.aws.resource.dynamodb.dynamodb

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource