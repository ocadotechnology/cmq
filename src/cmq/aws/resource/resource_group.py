import json
from cmq.aws.aws import AWSResource


class resource_group(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "resource-groups"
        self._resource = "resource-group"
        self._list_function = "search_resources"

    def search(self, resource_types: list = ["AWS::AllSupported"], **tags: dict) -> "resource_group":
        self._list_parameters = {
            "ResourceQuery": {
                "Type": "TAG_FILTERS_1_0",
                "Query": json.dumps({
                    "ResourceTypeFilters": resource_types,
                    "TagFilters": [
                        {
                            "Key": key,
                            "Values": [value]
                        } for key, value in tags.items()
                    ]
                })
            }
        }
        return self