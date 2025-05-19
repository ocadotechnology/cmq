
# Log Stream

The Log Stream resource provides access to AWS CloudWatch log streams.

## Usage

```python
from cmq.aws.session import profile

# List all log streams
profile().log_stream().list()
```

## Log Stream
::: cmq.aws.resource.log_stream.log_stream

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource