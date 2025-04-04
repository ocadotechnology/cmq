from cmq.aws.aws import AWSResource


class user_key(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "iam"
        self._resource = "key"
        self._list_function = "list_access_keys"
        self._list_key = "AccessKeyMetadata"

    def get_parameters(self, context: dict) -> dict:
        parameters = self._list_parameters.copy()
        if 'iam_user' in context:
            parameters["UserName"] = context["iam_user"]["UserName"]
        return parameters