from cmq.aws.aws import AWSResource


class elasticache_parameter_group(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "elasticache"
        self._resource = "elasticache_parameter_group"
        self._list_function = "describe_cache_parameter_groups"
        self._list_key = "CacheParameterGroups"
