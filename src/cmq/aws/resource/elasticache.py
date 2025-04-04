from typing import Any
from cmq.aws.aws import AWSResource
from cmq.aws.resource.elasticache_parameter_group import elasticache_parameter_group


class elasticache(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "elasticache"
        self._resource = "elasticache"
        self._list_function = "describe_cache_clusters"
        self._list_key = "CacheClusters"

        self._tag_function = "list_tags_for_resource"
        self._tag_function_key = "ResourceName"

        self._metric_namespace = "AWS/ElastiCache"
        self._metric_dimension_name = "CacheClusterId"
        self._metric_dimension_resource_key = "CacheClusterId"

    def parameter_group(self) -> AWSResource:
        return elasticache_parameter_group(self)

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["ARN"]
