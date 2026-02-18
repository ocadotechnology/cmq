# SNS

    The SNS Subscription resource provides access to AWS Simple Notification Service subscriptions.

## Usage

```python
from cmq.aws.session import profile

# List all SNS subscriptions
profile().sns_subscription().list()
```

## SNS Subscription
::: cmq.aws.resource.sns_subscription.sns_subscription

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource