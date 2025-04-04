from typing import Any
from cmq.aws.aws import AWSResource


class dynamodb(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "dynamodb"
        self._resource = "dynamodb"
        self._list_function = "list_tables"

        self._describe_function = "describe_table"
        self._describe_function_key = "TableName"
        self._describe_resource_key = "resource"

        self._tag_function = "list_tags_of_resource"
        self._tag_function_key = "ResourceArn"
        self._tag_resource_key = "resource"

        self._metric_namespace = "AWS/DynamoDB"
        self._metric_dimension_name = "TableName"
        self._metric_dimension_resource_key = "resource"

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource) -> str:
        return f"arn:aws:dynamodb:{context['aws_region']}:{context['aws_account']}:table/{resource['resource']}"
