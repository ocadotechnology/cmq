from typing import Any

from cmq.aws.aws import AWSResource
from cmq.aws.resource.restore_plan_job import restore_plan_job


class restore_plan(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "backup"
        self._resource = "restore_plan"
        self._list_function = "list_restore_testing_plans"


    def job(self) -> AWSResource:
        return restore_plan_job(self)

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["DBInstanceArn"]
