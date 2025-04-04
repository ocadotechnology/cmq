from typing import Any
from cmq.aws.aws import AWSResource


class alarm(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "cloudwatch"
        self._resource = "alarm"
        self._list_function = "describe_alarms"
        self._list_key = "MetricAlarms"

        self._tag_function = "list_tags_for_resource"
        self._tag_function_key = "ResourceARN"

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["AlarmArn"]
