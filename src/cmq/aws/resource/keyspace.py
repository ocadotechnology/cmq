from cmq.aws.aws import AWSResource
from cmq.aws.resource.keyspace_table import keyspace_table


class keyspace(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "keyspaces"
        self._resource = "keyspace"
        self._list_function = "list_keyspaces"
        self._list_key = "keyspaces"

    def table(self) -> AWSResource:
        return keyspace_table(self)