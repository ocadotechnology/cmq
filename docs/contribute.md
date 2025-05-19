# Contribute to the project

## Configure your environment

`cmq` uses `poetry` to manage dependencies. Poetry recommends to use a virtual environment, but it's not mandatory.

Clone the repository and install dependencies:

```bash
git clone https://github.com/ocadotechnology/cmq
cd cmq
poetry install
```

## How to add new resources

Adding support for a new resource is really simple. `cmq` uses a plugin system to load resources. You can add new sessions/resources to `cmq` directly or you can create your own packages. Let's see how to do it.

### Adding a new resource

Let's add a new resource to list IAM Users.

The first thing we have to do is create a new resource class. Create the file `user.py` inside the `src/cmq/aws/resource` folder with the following content:

```python
from cmq.aws.aws import AWSResource

class user(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "iam"
        self._resource = "user"
        self._list_function = "list_users"
        self._list_key = "Users"
```

* `_service`: This is the name of the AWS service
* `_resource`: This is a descriptive/short value to name the resource
* `_list_function`: The `boto3` function that list/describe the resource
* `_list_key`: The key that contains the results in the response. If this is not defined, `cmq` will try to find the list automatically.
* `_list_paginated`: `True` (default value) if the `boto3` function support pagination. `False` otherwise.


### Add the new class to the project entry point

Open the file `pyproject.toml` and add the following line to the section `[project.entry-points."cmq.provider.aws"]`:

```toml
user = "cmq.aws.resource.user:user"
```

### Using the new resource

We can start using the new resource to list IAM users. For example, let's list all users in `account-a` account:

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

All the filters are also compatible with the new resource. For example, we can retrieve only the attributes `UserName` and values that contains `test`.

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

Similarly to the list function, `cmq` provides a method to load tags as part of the resource definition. All we need to do is adding a few attributes/method that describe how tags are loaded.

Update the above class with the following details:

```python
from cmq.aws.aws import AWSResource

class user(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "iam"
        self._resource = "user"
        self._list_function = "list_users"
        self._list_key = "Users"

        self._tag_function = "list_user_tags"
        self._tag_function_key = "UserName"
        self._tag_resource_key = "UserName"
```

The new attributes are:

* `_tag_function`: The `boto3` function that list tags for this resource
* `_tag_function_key`: The parameter passed to the function to list the tags
* `_tag_resource_key`: The key that identify the resource in the response of `_list_function`

The `cmq` will automatically load the tags for the resource when you call the `tags()` action.

#### Managing tags

Sometimes getting the correct value for the tag function is a little bit more complex. For these cases, there are a couple of methods to handle the situation:

* `_get_tag_resource_identifier`: This method is called to get the value for the tag function. It receives the resource as a parameter and returns the value to be used in the tag function.
* `_format_tags`: This method is called to format the tags returned by the tag function. It receives the tags as a parameter and returns the formatted tags.

For example, the function that list tags for Kinesis streams expects to receive the ARN of the stream:

```python
    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["StreamARN"]
```

### Adding support for describe 

Sometimes the information available in the list function is not enough. In this case, you can add a describe function to retrieve the full information for a specific resource. A good example of this is is DynamoDB tables. DynamoDB tables are identified by the name, but the list function only returns the name of the table. To get the full information, we need to use the describe function.

```python
        self._describe_function = "describe_table"
        self._describe_function_key = "TableName"
        self._describe_resource_key = "resource"
```

The new attributes are:

* `_describe_function`: The `boto3` function that describe the resource
* `_describe_function_key`: The parameter passed to the function to describe the resource
* `_describe_resource_key`: The key that identify the resource in the response of `_list_function`

When you call the `describe` action, `cmq` will use the `_describe_function` to retrieve the full information for the resource.

Now, we can retrieve the full information for all tables that start with `users-`:

```bash
cmq 'profile().dynamodb().starts_with("resource", "users-").describe().list()'
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

Now we can get RDS metrics for this resource. For example, let's get the maximum `CPUUtilization` of `webserver` databases:

```python
profile().rds().tags().eq("Tags.appId", "webserver").metric(statistic="Maximum", metric_name="CPUUtilization", unit="Percent")
```