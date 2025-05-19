
# KMS Alias

The KMS Alias resource provides access to AWS KMS aliases.

## Usage

```python
from cmq.aws.session import profile

# List all KMS aliases
profile().kms_alias().list()
```

## KMS Alias
::: cmq.aws.resource.kms_alias.kms_alias

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource