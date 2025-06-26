import json
from cmq.aws.aws import AWSResource


class security_group(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "ec2"
        self._resource = "security-group"
        self._list_function = "describe_security_groups"
