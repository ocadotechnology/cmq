from typing import Any
from cmq.aws.aws import AWSResource


class sns(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "sns"
        self._resource = "sns"
        self._list_function = "list_topics"

        self._tag_function = "list_tags_for_resource"
        self._tag_function_key = "ResourceArn"

        self._metric_namespace = "AWS/SNS"
        self._metric_dimension_name = "TopicName"
        self._metric_dimension_resource_key = "TopicName"

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["TopicArn"]
