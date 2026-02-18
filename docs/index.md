# Cloud Multi Query

Cloud Multi Query (CMQ) is a Python library & CLI tool that allows you to run the same query across multiple cloud accounts in parallel, making it easy to gather insights and manage multi-account environments efficiently.

So far, CMQ only supports AWS cloud accounts. However, the plugable structure of CMQ allows for the creation of new session and resource types to include other cloud providers.

## Requirements

1. AWS Config profiles created for each account

## Setup

Install the package:

```bash
pip install cmq
```

## Basic usage

### Introduction

`cmq` uses resource chain calls to retreive information from AWS Accounts. The format is as follows:

```bash
 profile().rds().parameter_group().list()
|---------|-----------------------|------|
  session      resource chain      action
```

The first object is always a `session` class. This class is the responsible to configure a `boto3` session object for the objects in the resource chain.

The resource chain is an optional ordered list of resources calls. For example, in the resource chain above we get all the RDS resources and for each of the them, we get the RDS parameter groups. The operations defined in the resource chain are executed in parallel for each account retrieved by the session object.

Both `session` and `resource chain` support additional calls to filter/manage the results. These operation are executed in order, so filtering resources in the request is more efficient than filtering the results in the response.

Finally, the last call in the chain is the `action` and defines what do we want to do with the results.
There are two basic actions: `list` and `dict`, which returns the results using different types.
Other resources support more actions and they are described in the resource class.

Let's see some examples.

### Getting accounts

We can start by getting the list of accounts (profiles) defined in your local configuration:

```python
from cmq.aws.session.profile import profile
profile().list()
```

As you can see, the `resource chain` is empty in this example (it's an optional part of the chain).

CMQ also supports a CLI interface to run queries.

```bash
cmq 'profile().rds().list()'
```

### Enable verbose output

We can export the environment variable `CMQ_VERBOSE_OUTPUT=true` to show the progress of the query.

```bash
> cmq 'profile().elasticache().list()'
 100.00% :::::::::::::::::::::::::::::::::::::::: |        1 /        1 |:  account-a         elasticache
 100.00% :::::::::::::::::::::::::::::::::::::::: |        1 /        1 |:  account-b         elasticache
 100.00% :::::::::::::::::::::::::::::::::::::::: |        1 /        1 |:  account-c         elasticache
 100.00% :::::::::::::::::::::::::::::::::::::::: |        1 /        1 |:  account-d         elasticache
 100.00% :::::::::::::::::::::::::::::::::::::::: |        1 /        1 |:  account-e         elasticache
```

Using the `--verbose` flag in the CLI produce the same result.

### Filtering accounts

We can also apply some filters in the request, so not all the accounts are processed. In the case of the `profile` session class, we can filter only by name:

Filter all profiles starting with `test`:

```python
profile(name="test").list()
```

## Listing resources

Now that we know how to get accounts, let's get some AWS resources.

### Supported resources

Currently, the supported resources are:

* Elastic IPs (address)
* CloudWatch alarms
* CloudWatch metrics
* CloudWatch logs
* CloudTrail events
* DynamoDB tables
* Elasticache clusters
* Elasticache replication groups
* Elasticache parameter groups
* Elasticache subnet groups
* Functions (lambdas)
* Keyspaces
* Keyspaces tables
* Kinesis streams
* KMS keys
* RDS databases
* RDS parameter groups
* Regions
* Resource Explorer
* Resource groups
* Route53 Hosted Zones
* S3 buckets
* S3 objects (experimental)
* SecretsManager secrets
* SNS topics
* SNS subscriptions
* SQS queues
* IAM users
* IAM user keys
* IAM roles
* VPC

### Getting a list of resources

For example, let's get the list of `sns` topics in `account-c` account:

```python
profile(name="account-c").sns().list()
```

If we remove the filter name, we will get all the `sns` topics in all accounts:

```python
profile().sns().list()
```

### Configuring the resources attributes

We can use `attr` to reduce the number of fields returned by the AWS resources. For example, if we are only interested in the `FunctionName` of the `lambda` functions:

```python
profile().function().attr("FunctionName").list()
```

### Mapping resources to accounts

Sometimes it's useful to have the list of resources grouped by the account name. We can use `dict()` action in this case:

```python
profile().sns().dict()
```

### Listing resources in all enabled regions

To list resources in all enabled regions, you can use the `region` resource. This will retrieve regions available in each account and then list the resources in each region.

For example, to list all `sns` topics in all regions for each account, you can do the following:
```python
profile().region().sns().list()
```

You can also limit the regions to a specific list using the `regions` parameter:

```python
profile().region(regions=["us-east-1", "eu-west-1"]).sns().list()
```

### Listing resources in CSV format

Lists and dictionaries are ideal when you are going to process the data programatically. In the other hand, if you want to take a look at the data manually or visualize it in a tool like a spreadsheet, it's better to use a CSV format.

For these cases, you can use the `csv()` action. The action will also include a `session` keyword with the name of the session used to get the resource.

```bash
cmq --verbose 'profile().elasticache().csv()' --output elasticache.csv
```

### Filtering resources in the request

Similarly to the `profile` session class, you can filter the resources while doing the request. In this case, the parameters specified in the filter will be used by the `boto3` function that lists that specific resource. Each resource class uses a different `boto3` function to list the resources.

For example, for the `sqs` resource the function `list_queues` is used. So we can use `QueueNamePrefix` to filter some queues before processing them with `cmq`:

```python
profile().sqs(QueueNamePrefix="webserver-").list()
```

### Limiting resources in the request

Sometimes the volume of data returned by AWS is overwhelming and you'd prefer to get only a maximum amount of resources. For these cases you can use the `limit` function:

```python
profile().sqs().limit(10).list()
```

This query will return the first 10 queues for each account. This functionality only works with paginated resources.

### Filtering resources in the response

Many times, the session/resource object you want to list does not support filtering by a specific attribute.
In this case, you can use the `filter` function to reduce the number of resources that are processed in the response and focus on the resources that you are interested in.

The function `filter` receives a single function as argument and it should return `True` if you want to keep the resource or `False` if we want to get rid of it.

For example, this will retrieve all the queues that contains `backup` in all accounts:

```python
profile().sqs().filter(lambda r: "backup" in r["resource"]).list()
```

You can call multiple times to the `filter` function, and all the filters will be applied to the resources in the order specified.

### Quick filters

There is a list of quick filters already defined for convenience.

* eq
* ne
* in_
* contains
* not_contains
* starts_with
* ends_with
* gt
* lt

All the functions have two arguments: `(key, value)`. `key`, is the name of the key that you want to evaluate
as part of the filter and `value` the value you'll use to perform the comparison.

The `key` argument support dict/list path ([python-benedict](https://pypi.org/project/python-benedict/)).

For example, let's filter `elasticache` resources using the default `default.redis` parameter group names:

```python
profile().elasticache().starts_with("CacheParameterGroup.CacheParameterGroupName", "default.redis").list()
```

### Transform of values

Sometimes the values in the response from AWS does not have the right type or format to work with them. With
`cmq` you can easily tranform fields into new types. A good example of this are serialised `json` objects.


```python
import json
profile().cloudtrail().transform("CloudTrailEvent", json.loads).list()
```

We are instructing `cmq` to transform the field `CloudTrailEvent` (that we know contains a json
serialisable object) in all the resources using `json.loads` method. This is useful if you want to process or filter the information later on.

### Calculate fields

Similarly to the transformed values, you can also create new attributes (or overwrite existing ones)
that will be computed using the resource details.

For example, this list KMS keys and will add a new field in the resource root dictionary:

```python
profile().kms().describe().calculate("CreationDate", lambda x: x["Describe"]["KeyMetadata"]["CreationDate"]).attr("KeyId", "CreationDate").list()
```

## Getting tags

Many resources in AWS support tags, but usually the tags are not loaded as part of the resource definition. You can use the `tags()` function to instruct `cmq` to load the tags as part of the retrieval. If the resource does not support tags, the call to this function will be ignored.

The tags will be loaded as part of the resource definition, in the `Tags` key.

For example, let's get all sqs including their tags:

```python
profile().sqs().tags().list()
```

We can not use `tags` to filter resources in the request, but we can use it to filter resources in the response
with the `filter` function or the quick filters. For example, filter queues assigned to `alpha` team:

```python
profile().sqs().tags().filter(lambda r: r.get("Tags", {}).get("teamId") == "alpha").list()
```

You can also use quick filters to get the same results:

```python
profile().sqs().tags().eq("Tags.teamId", "alpha").list()
```

## Getting metrics

Many resources provisioned in AWS publish metrics about their usage to `CloudWatch`. `cmq` offers a `metric` resource that
you can use get this information, but it's also possible to get metrics from other resource types. This is more
convinient in most of the cases. Similarly to the tags, not all the resources support  the `metric` function.

These are the parameters and their default values:

* **statistic**: Name of the staticstic to use (e.g.:Minimum, Average, Maximum...)
* **metric_name**: Name of the metric (e.g.: CPUUtilization)
* **period**: Metric interval. **Default**: 1h
* **unit**: Metric unit. **Default**: "Count"
* **start_time**: Time of the first metric. **Default**: 90 days ago
* **end_time**: Time of the last metric. **Default**: current date

Let's take a look at some examples.

Get maximum `CPUUtilization` of `webserver` databases:

```python
profile().rds().tags().eq("Tags.appId", "webserver").metric(statistic="Maximum", metric_name="CPUUtilization", unit="Percent")
```

Number of `Invocations` of all lambda functions in all accounts:

```python
profile().function().metric(statistic="Sum", metric_name="Invocations")
```

### Plot the metrics

Looking at the raw metric data is not always easy so `cmq` also offers a `plot` function that will
create a graph for visualization. `plot` function uses the same parameters as the `metric` function and
adds a new one to manage the scale of the units:

* **unit_factor**: division factor. **Default**: 1. (e.g.: 1024 to show kilobytes instead of bytes)

For example, let's get the number of invocations of `send_email` lambda in all account:

```python
profile().function().contains("FunctionName", "send_email").plot(statistic="Sum", metric_name="Invocations")
```