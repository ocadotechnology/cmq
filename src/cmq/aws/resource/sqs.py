from typing import Any
from cmq.aws.aws import AWSResource


class sqs(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "sqs"
        self._resource = "sqs"
        self._list_function = "list_queues"
        self._list_key = "QueueUrls"

        self._describe_function = "get_queue_attributes"
        self._describe_function_key = "QueueUrl"
        self._describe_resource_key = "resource"

        self._tag_function = "list_queue_tags"
        self._tag_function_key = "QueueUrl"

        self._metric_namespace = "AWS/SQS"
        self._metric_dimension_name = "QueueName"
        self._metric_dimension_resource_key = "resource"

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["resource"]

    def _get_tag_from_result(self, result):
        return result.get("Tags", {})

    def _format_tags(self, tags) -> dict:
        return {"Tags": tags}

    def _describe(self, context, client, resource):
        describe_function = getattr(client, self._describe_function)
        describe_identifier = self._get_describe_resource_identifier(context, resource)
        details = describe_function(**{self._describe_function_key: describe_identifier}, AttributeNames=["All"])
        resource.update({"Describe": details.get("Attributes", {})})