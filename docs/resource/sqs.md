# SQS

The SQS resource provides access to AWS Simple Queue Service queues.

## Usage

```python
from cmq.aws.session import profile

# List all SQS queues
profile().sqs().list()
```

## SQS
::: cmq.aws.resource.sqs.sqs

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource