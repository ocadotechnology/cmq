from typing import Any
from cmq.aws.aws import AWSResource


class elasticache_replication_group(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "elasticache"
        self._resource = "elasticache_replication_group"
        self._list_function = "describe_replication_groups"
        self._list_key = "ReplicationGroups"
        self._tag_function = "list_tags_for_resource"
        self._tag_function_key = "ResourceName"

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["ARN"]
