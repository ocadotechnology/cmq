from datetime import datetime
from datetime import timezone
from datetime import timedelta
from cmq.aws.aws import AWSResource


class restore_plan_job(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "backup"
        self._resource = "restore_plan_job"
        self._list_function = "list_restore_jobs"

    def get_parameters(self, context: dict) -> dict:
        parameters = self._list_parameters.copy()
        if 'backup_restore_plan' in context:
            parameters["ByRestoreTestingPlanArn"] = context["backup_restore_plan"]["RestoreTestingPlanArn"]
        return parameters

    def created_after(self, **kwargs) -> "restore_plan_job":
        """
        Sets the 'ByCreatedAfter' parameter for filtering restore plan jobs.
        """
        self._list_parameters.update({"ByCreatedAfter": datetime.now(tz=timezone.utc) - timedelta(**kwargs)})
        return self
