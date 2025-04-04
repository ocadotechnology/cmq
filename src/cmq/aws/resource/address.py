from cmq.aws.aws import AWSResource


class address(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "ec2"
        self._resource = "address"
        self._list_function = "describe_addresses"
        self._list_key = "Addresses"
        self._list_paginated = False
