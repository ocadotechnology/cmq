from typing import Any
from cmq.aws.aws import AWSResource


class vpc(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "ec2"
        self._resource = "vpc"
        self._list_function = "describe_vpcs"

        self._describe_function = "describe_vpcs"
        self._describe_function_key = "VpcIds"
        self._describe_resource_key = "VpcId"
