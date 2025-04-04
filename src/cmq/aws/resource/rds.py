from typing import Any

from cmq.aws.aws import AWSResource
from cmq.aws.resource.rds_parameter_group import rds_parameter_group


class rds(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "rds"
        self._resource = "rds"
        self._list_function = "describe_db_instances"

        self._tag_function = "list_tags_for_resource"
        self._tag_function_key = "ResourceName"

        self._metric_namespace = "AWS/RDS"
        self._metric_dimension_name = "DBInstanceIdentifier"
        self._metric_dimension_resource_key = "DBInstanceIdentifier"

    def parameter_group(self) -> AWSResource:
        return rds_parameter_group(self)

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["DBInstanceArn"]
