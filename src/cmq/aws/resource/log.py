from cmq.aws.aws import AWSResource
from cmq.aws.resource.log_stream import log_stream
from cmq.aws.resource.log_event import log_event


class log(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "logs"
        self._resource = "log-group"
        self._list_function = "describe_log_groups"

        self._tag_function = "list_tags_for_resource"
        self._tag_function_key = "resourceArn"
        self._tag_resource_key = "logGroupArn"

    @property
    def stream(self) -> log_stream:
        return log_stream(self)

    @property
    def event(self, **kwargs) -> log_event:
        return log_event(self).__call__(**kwargs)

    def _get_tag_from_result(self, result) -> list:
        return result.get("tags", {})

    def _format_tags(self, tags) -> dict:
        return {"Tags": tags}