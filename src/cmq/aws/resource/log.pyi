from cmq.aws.aws import AWSResource as AWSResource
from cmq.aws.resource.log_event import log_event as log_event
from cmq.aws.resource.log_stream import log_stream as log_stream

class log(AWSResource):
    def __init__(self, parent=None) -> None: ...
    @property
    def stream(self) -> log_stream: ...
    @property
    def event(self, **kwargs) -> log_event: ...
