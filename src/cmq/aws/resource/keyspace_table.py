from cmq.aws.aws import AWSResource


class keyspace_table(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "keyspaces"
        self._resource = "table"
        self._list_function = "list_tables"
        self._list_key = "tables"

        self._describe_function = "get_table"

    def get_parameters(self, context: dict) -> dict:
        parameters = self._list_parameters.copy()
        if 'keyspaces_keyspace' in context:
            parameters["keyspaceName"] = context["keyspaces_keyspace"]["keyspaceName"]
        return parameters

    def _describe(self, context, client, resource):
        describe_function = getattr(client, self._describe_function)
        details = describe_function(keyspaceName=resource["keyspaceName"],
                                    tableName=resource["tableName"])
        resource.update({"Describe": details})