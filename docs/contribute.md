# Contribute to the project

## Configure your environment

`cmq` uses `poetry` to manage dependencies. It's recommended to use a virtual environment.

Run the following commands to prepare the environment:

```bash
pip install poetry
poetry install
```

## How to add new resources

Adding support for a new resource is as simple as create a new module as part of the `cmq.aws.resource` package with the following information:

* The AWS Service where the resource belongs to
* The Boto3 function that list/describe the resource
* *[OPTIONAL]* The Boto3 function that get the tags for the resource
* *[OPTIONAL]* The CloudWatch Metric namespace and dimension for the resource

### Adding a new resource

Let's add a new resource for IAM Users.

The first thing we have to do is create a new resource module. Create the file `user.py` inside the `src/cmq/aws/resource` folder with the following content:

```python
from cmq.aws.aws import Resource


class user(Resource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "iam"
        self._resource = "user"
        self._list_function = "list_users"
        self._list_key = "Users"
```

*The name of the module and the name of the class should be the same (`user.py` & `user` classname).*

* `_service`: This is the name of the AWS service
* `_resource`: This is a descriptive/short value to name the resource
* `_list_function`: The `boto3` function that list/describe the resource
* `_list_key`: The key that contains the results in the response. If this is not defined, cmq will try to find the list automatically.
* `_list_paginated`: `True` (default value) if the `boto3` function support pagination. `False` otherwise.


### Using the new resource

You can start using the new resource to list IAM users now. For example, let's list all users in `account-a` account:

```bash
cmq 'profile(name="account-a").user().list()'
[
  {
    "Path": "/",
    "UserName": "user.a",
    "UserId": "XXXXXXXXXXXXXX",
    "Arn": "arn:aws:iam::123456789012:user/user.a",
    "CreateDate": "2024-05-29 21:17:17+00:00"
  },
...
```

All the filters functions are also applicable to the new resource. For example, we can filter the attributes only to `UserName` and values that contains `test`.

```bash
cmq 'profile(name="account-a").user().attr("UserName").contains("UserName", "test").list()'
[
  {
    "UserName": "test-web"
  },
  {
    "UserName": "test-backend"
  }
]
```

### Adding support for tags

Many of the AWS resources support tags. Adding support to load tags as part of your new resource is similar listing the resource. All we need to do is adding a few attributes/method that describe how the tags are loaded.

Update the above class with the following details:

```python
from cmq.aws.aws import Resource


class user(Resource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "iam"
        self._resource = "user"
        self._list_function = "list_users"
        self._list_key = "Users"

        self._tag_function = "list_user_tags"
        self._tag_function_key = "UserName"
```

The new attributes are:

* `_tag_function`: The `boto3` function that list tags for this resource
* `_tag_function_key`: The parameter passed to the function to list the tags

#### Resource identifier for tag function

Usually, the value of `_tag_function_key` is also the key that identify the resource in the response of `_list_function`.
For example, in the case of IAM user, the list function `list_users` returns a list of dictionaries where each user is identified by the key `UserName`, which is also the parameter for the function `list_user_tags`.

If that's not the case, you'd need to define how the value is calculated from the list response by implementing the `_get_tag_resource_identifier` function. For example, the function that list tags for Kinesis streams expects to receive the ARN of the stream:

```python
    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["StreamARN"]
```

#### Tag format

`cmq` manages automatically the response of the function that list the tags, as long the response uses the standard format:

```python
{
    'Tags': [
        {
            'Key': 'string',
            'Value': 'string'
        },
    ],
    'IsTruncated': True|False,
    'Marker': 'string'
}
```

If that's not the case, you'd need to implement the function to format properly the tags for your resource.
You can do so by implementing the `_format_tags` method. For example, `kms` list tag function uses a different format, so you can implement the function to keep the same format:

```python
    def _format_tags(self, tags) -> dict:
        return {"Tags": {tag["TagKey"]: tag["TagValue"] for tag in tags}}
```


### Adding support for metrics

AWS publish CloudWatch metrics to allow users monitor the usage of their services. You can use the `metric` module to access this information, but other modules can also define some attributes that will simplify the process of getting metrics for that specific resource. For example, the `rds` resource defines:

```python
    self._metric_namespace = "AWS/RDS"
    self._metric_dimension_name = "DBInstanceIdentifier"
    self._metric_dimension_resource_key = "DBInstanceIdentifier"
```

* `_metric_namespace`: This is the namespace of the metric in CloudWatch
* `_metric_dimension_name`: This is the dimension inside the namespace
* `_metric_dimension_resource_key`: This is the resource key that need to be used in the dimension
