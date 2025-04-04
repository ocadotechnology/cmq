# Cloud Multi Query

Cloud Multi Query is a Python library & CLI tool that allows you to run the same query across multiple cloud accounts in parallel, making it easy to gather insights and manage multi-account environments efficiently.

So far, CMQ only supports AWS cloud accounts. However, the plugable structure of CMQ allows for the creation of new session and resource types to include other cloud providers.

## Installation

```
pip install cmq
```

## Basic usage

CMQ works using profiles defined in your local machine ([AWS CLI configuration](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html)). It's expected that every profile defines the access to an account/region.

Let's start listing the configured profiles:

```bash
cmq 'profile().list()'
[
   {
    "name": "account_a",
    "region": "us-east-1"
  },
  {
    "name": "account_b",
    "region": "eu-west-1"
  }
]
```

We can list resources for these accounts. CMQ will execute the queries in parallel. For example, lets list RDS resources:

```bash
cmq 'profile().rds().list()'
[
 {
    "DBInstanceIdentifier": "account-a-users",
    "DBInstanceClass": "db.m6g.large",
    "Engine": "postgres",
    ...
 },
 {
    "DBInstanceIdentifier": "account-b-users",
    "DBInstanceClass": "db.m6g.large",
    "Engine": "postgres",
    ...
 },
 ...
]
```

We can also use `cmq` as a Python library. This is more convenient when you need to process the results:

```python
>>> from cmq.aws.session.profile import profile
>>> profile().sqs().list()
[
 {"resource": "https://sqs.us-east-1.amazonaws.com/123456789012/account-a-products"},
 {"resource": "https://sqs.us-east-1.amazonaws.com/123456789012/account-a-orders"},
 {"resource": "https://sqs.eu-west-1.amazonaws.com/210987654321/account-b-products"},
 {"resource": "https://sqs.eu-west-1.amazonaws.com/210987654321/account-b-orders"}
]
```

## Enable verbose output

We can export the environment variable `CMQ_VERBOSE_OUTPUT=true` or use the option `verbose` in the CLI to output the progress of the query. This is particular useful when you have many accounts to process:

```bash
cmq --verbose 'profile().elasticache().list()'
 100.00% :::::::::::::::::::::::::::::::::::::::: |        1 /        1 |:  account-dev     elasticache
 100.00% :::::::::::::::::::::::::::::::::::::::: |        1 /        1 |:  account-test    elasticache
 100.00% :::::::::::::::::::::::::::::::::::::::: |        1 /        1 |:  account-prd1    elasticache
 100.00% :::::::::::::::::::::::::::::::::::::::: |        1 /        1 |:  account-prd2    elasticache
 100.00% :::::::::::::::::::::::::::::::::::::::: |        1 /        1 |:  account-prd3    elasticache
[
    ... resource list ...
]
```

## Examples

While we work on the full documentation, we'll share some example queries to give you an idea of what you can do with the tool:

List RDS resources in one profile with name `account_a`
```bash
cmq 'profile(name="account_a").rds().list()'
```

List SNS topics for all profiles, but returning a dictionary where the key is the name of the profile:
```bash
cmq 'profile().sns().dict()'
{
    "account_a": [
        ... topics from account a ...
    ],
     "account_b": [
        ... topics from account b ...
    ],
}
```

List all roles for all accounts, but return only the `RoleName` field:
```bash
cmq 'profile().role().attr("RoleName").list()'
```

List DynamoDB tables, but limit the results to 10 tables:
```bash
cmq 'profile().dynamodb().limit(10).list()'
```

CMQ uses `boto3` to list/describe resources. You can also use the parameters of the `boto3` functions to filter resources in the request. For example, this will list all SQS queues with prefix `order` in all accounts:

```bash
cmq 'profile().sqs(QueueNamePrefix="order").list()'
```

We can also filter resources in the response. CMQ is built with a set of quick filters that you can use with any resource type. All the filters have the same structure: `__filter__(key, value)`

For example, the following query list Lambda functions running with `python3.10` in all accounts:

```bash
cmq 'profile().function().eq("Runtime", "python3.10").list()'
```

These are the supported quick filters:

* eq
* ne
* in_
* contains
* not_contains
* starts_with
* ends_with
* gt
* lt

## Supported resources

AWS
* address
* alarm
* cloudformation
* cloudtrail
* dynamodb
* ec2
* elasticache_parameter_group
* elasticache_replication_group
* elasticache_subnet_group
* elasticache
* function
* kinesis
* kms_alias
* kms
* log_event
* log_stream
* log
* metric
* rds_parameter_group
* rds
* resource_explorer
* resource_group
* role
* s3_object
* s3
* sns
* sqs
* user_key
* user
