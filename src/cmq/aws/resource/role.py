from cmq.aws.aws import AWSResource


class role(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "iam"
        self._resource = "role"
        self._list_function = "list_roles"
        self._list_key = "Roles"

        self._tag_function = "list_role_tags"
        self._tag_function_key = "RoleName"
        self._tag_resource_key = "RoleName"

        self._describe_function = "get_role"
        self._describe_function_key = "RoleName"
        self._describe_resource_key = "RoleName"
