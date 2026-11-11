from cmq.aws.aws import AWSResource as AWSResource
from cmq.aws.resource.user_key import user_key as user_key
from typing import Any

class user(AWSResource):
    def __init__(self, parent=None) -> None: ...
    def key(self, **kwargs: dict[str, Any]) -> user_key: ...
