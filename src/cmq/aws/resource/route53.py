from typing import Any
from cmq.aws.aws import AWSResource


class route53(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "route53"
        self._resource = "route53"
        self._list_function = "list_hosted_zones"

        self._tag_function = "list_tags_for_resource"
        self._tag_function_key = "ResourceId"
        self._tag_function_resource_type = "hostedzone"

        self._describe_function = "get_hosted_zone"
        self._describe_function_key = "Id"
        self._describe_resource_key = "Id"

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource) -> str:
        return resource["Id"]

    def _format_tags(self, tags) -> dict:
        return {"Tags": {tag["Key"]: tag["Value"] for tag in tags["ResourceTagSet"]["Tags"]}}
