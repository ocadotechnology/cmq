from typing import Any
from cmq.aws.aws import AWSResource
from cmq.aws.resource.kms_alias import kms_alias


class kms(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "kms"
        self._resource = "kms"
        self._list_function = "list_keys"

        self._tag_function = "list_resource_tags"
        self._tag_function_key = "KeyId"

        self._describe_function = "describe_key"
        self._describe_function_key = "KeyId"
        self._describe_resource_key = "KeyId"

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource) -> str:
        return resource["KeyId"]

    def _format_tags(self, tags) -> dict:
        return {"Tags": {tag["TagKey"]: tag["TagValue"] for tag in tags}}

    def aliases(self) -> AWSResource:
        return kms_alias(self)