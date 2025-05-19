# Secret

The Secret resource provides access to AWS SecretsManager secrets.

## Usage

```python
from cmq.aws.session import profile

# List all secrets
profile().secret().list()
```

## Secret
::: cmq.aws.resource.secret.secret

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource