# Kinesis

The Kinesis resource provides access to AWS Kinesis streams.

## Usage

```python
from cmq.aws.session import profile

# List all Kinesis streams
profile().kinesis().list()
```

## Kinesis
::: cmq.aws.resource.kinesis.kinesis

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource