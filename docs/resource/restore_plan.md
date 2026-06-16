# Restore Plan

The Restore Plan resource provides access to AWS Restore Plans.

## Usage

```python
from cmq.aws.session import profile

# List all Restore Plans
profile().restore_plan().list()
```

## Restore Plan Jobs
::: cmq.aws.resource.restore_plan_job.restore_plan_job

## Inherited from ResourceInterface
::: cmq.base.ResourceInterface
## Inherited from Resource
::: cmq.base.Resource