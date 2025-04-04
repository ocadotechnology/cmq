from cmq.aws.aws import AWSResource


class log_event(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "logs"
        self._resource = "log-event"
        self._list_function = "filter_log_events"
        self._list_paginated = False

    def get_parameters(self, context: dict) -> dict:
        parameters = self._list_parameters.copy()
        if 'logs_log-group' in context:
            parameters["logGroupName"] = context["logs_log-group"]["logGroupName"]
        if 'logs_log-stream' in context:
            parameters["logStreamNames"] = [context["logs_log-stream"]["logStreamName"]]
        return parameters
