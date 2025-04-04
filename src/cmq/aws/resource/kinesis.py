from typing import Any
from cmq.aws.aws import AWSResource


class kinesis(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "kinesis"
        self._resource = "kinesis"
        self._list_function = "list_streams"
        self._list_key = "StreamSummaries"

        self._tag_function = "list_tags_for_stream"
        self._tag_function_key = "StreamARN"

        self._metric_namespace = "AWS/Kinesis"
        self._metric_dimension_name = "StreamName"
        self._metric_dimension_resource_key = "StreamName"

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["StreamARN"]
