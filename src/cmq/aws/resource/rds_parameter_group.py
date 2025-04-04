from typing import Any
from cmq.aws.aws import AWSResource


class rds_parameter_group(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "rds"
        self._resource = "rds_parameter_group"
        self._list_function = "describe_db_parameter_groups"
        self._list_key = "DBParameterGroups"

        self._tag_function = "list_tags_for_resource"
        self._tag_function_key = "ResourceName"

    def get_parameters(self, context: dict) -> dict:
        parameters = self._list_parameters.copy()
        if 'rds_rds' in context:
            parameters["DBParameterGroupName"] = context["rds_rds"]["DBInstanceIdentifier"]
        return parameters

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return f"arn:aws:rds:{context['aws_region']}:{context['aws_account']}:pg:{resource['DBParameterGroupName']}"
