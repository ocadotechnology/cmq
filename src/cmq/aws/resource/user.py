from typing import Any
from cmq.aws.aws import AWSResource
from cmq.aws.resource.user_key import user_key


class user(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "iam"
        self._resource = "user"
        self._list_function = "list_users"
        self._list_key = "Users"

        self._tag_function = "list_user_tags"
        self._tag_function_key = "UserName"
        self._tag_resource_key = "UserName"

    def key(self, **kwargs: dict[str, Any]) -> user_key:
        """
        Returns the resource for the user keys.

        Args:
            **kwargs (dict[str, Any]): Additional keyword arguments.

        Returns:
            user_key: Resource user keys.

        """
        return user_key(self).__call__(**kwargs)