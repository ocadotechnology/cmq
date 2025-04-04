from cmq.aws.aws import AWSResource


class s3_object(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "s3"
        self._resource = "object"
        self._list_function = "list_objects_v2"

    def get_parameters(self, context: dict) -> dict:
        parameters = self._list_parameters.copy()
        if 's3_bucket' in context:
            parameters["Bucket"] = context["s3_bucket"]["Name"]
        return parameters