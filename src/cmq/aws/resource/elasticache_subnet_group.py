from cmq.aws.aws import AWSResource


class elasticache_subnet_group(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "elasticache"
        self._resource = "elasticache_subnet_group"
        self._list_function = "describe_cache_subnet_groups"
        self._list_key = "CacheSubnetGroups"
