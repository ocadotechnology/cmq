from cmq.aws.aws import AWSResource


class resource_explorer(AWSResource):
    """
    A class representing a resource explorer.

    This class extends the base Resource class and provides functionality
    for exploring resources.

    Attributes:
        _service (str): The service name for the resource explorer.
        _resource (str): The resource name for the resource explorer.
        _list_function (str): The list function name for the resource explorer.
        _list_key (str): The list key for the resource explorer.

    Methods:
        get_parameters: Get the parameters for the resource explorer.

    Note:
        If the resource explorer is loaded from the application session,
        it will automatically filter resources based on the app_context_id
        of the application.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "resource-explorer-2"
        self._resource = "resource-explorer"
        self._list_function = "search"
        self._list_key = "Resources"

    def get_parameters(self, context: dict) -> dict:
        parameters = self._list_parameters.copy()
        if 'app_context_id' in context:
            parameters["QueryString"] = " ".join([
                parameters.get("QueryString", ""),
                f"tag:app_context_id={context['app_context_id']}",
            ])
        return parameters