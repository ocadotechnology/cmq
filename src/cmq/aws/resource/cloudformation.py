from cmq.aws.aws import AWSResource


class cloudformation(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "cloudformation"
        self._resource = "stack"
        self._list_function = "list_stacks"
