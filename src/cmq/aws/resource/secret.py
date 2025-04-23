from cmq.aws.aws import AWSResource


class secret(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "secretsmanager"
        self._resource = "secrets"
        self._list_function = "list_secrets"
        self._list_key = "SecretList"
