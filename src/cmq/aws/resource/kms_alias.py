from cmq.aws.aws import AWSResource


class kms_alias(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "kms"
        self._resource = "kms_alias"
        self._list_function = "list_aliases"

    def get_parameters(self, context: dict) -> dict:
        parameters = self._list_parameters.copy()
        if 'kms_kms' in context:
            parameters["KeyId"] = context["kms_kms"]["KeyId"]
        return parameters
