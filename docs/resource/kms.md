
# KMS

The KMS resource provides access to AWS KMS keys.

## Usage

```python
from cmq.aws.session import profile

# List all KMS keys
profile().kms().list()
```

## KMS
::: cmq.aws.resource.kms.kms

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource