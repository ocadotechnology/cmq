from typing import Any
from cmq.aws.aws import AWSResource


class function(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "lambda"
        self._resource = "function"
        self._list_function = "list_functions"
        self._list_key = "Functions"

        self._tag_function = "list_tags"
        self._tag_function_key = "Resource"

        self._metric_namespace = "AWS/Lambda"
        self._metric_dimension_name = "FunctionName"
        self._metric_dimension_resource_key = "FunctionName"

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["FunctionArn"]

    def _get_tag_from_result(self, result):
        return result.get("Tags", {})

    def _format_tags(self, tags) -> dict:
        return {"Tags": tags}