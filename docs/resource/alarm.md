# Alarm

The Alarm resource provides access to AWS CloudWatch alarms.

## Usage

```python
from cmq.aws.session import profile

# List all alarms
profile().alarm().list()
```

## Alarm
::: cmq.aws.resource.alarm.alarm

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource