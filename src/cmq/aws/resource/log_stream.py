from cmq.aws.aws import AWSResource
from cmq.aws.resource.log_event import log_event


class log_stream(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "logs"
        self._resource = "log-stream"
        self._list_function = "describe_log_streams"

    def get_parameters(self, context: dict) -> dict:
        parameters = self._list_parameters.copy()
        if 'logs_log-group' in context:
            parameters["logGroupName"] = context["logs_log-group"]["logGroupName"]
        return parameters

    def event(self, **kwargs) -> log_event:
        return log_event(self).__call__(**kwargs)