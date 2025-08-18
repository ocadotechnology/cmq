from typing import Any
from cmq.aws.aws import AWSResource


class rds_parameter(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "rds"
        self._resource = "rds_parameter"
        self._list_function = "describe_db_parameters"
        self._list_key = "Parameters"

    def get_parameters(self, context: dict) -> dict:
        parameters = self._list_parameters.copy()
        if 'rds_rds_parameter_group' in context:
            parameters["DBParameterGroupName"] = context["rds_rds_parameter_group"]["DBParameterGroupName"]
        return parameters
