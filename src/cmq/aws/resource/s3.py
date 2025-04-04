from typing import Any

from cmq.aws.aws import AWSResource
from cmq.aws.resource.s3_object import s3_object


class s3(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "s3"
        self._resource = "bucket"
        self._list_function = "list_buckets"

        self._tag_function = "get_bucket_tagging"
        self._tag_function_key = "Bucket"

        self._metric_namespace = "AWS/S3"
        self._metric_dimension_name = "BucketName"
        self._metric_dimension_resource_key = "Name"

    def objects(self, **kwargs) -> AWSResource:
        return s3_object(self)(**kwargs)

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["Name"]

    def _get_pages(self, context) -> Any:
        client = self.get_client(context)
        callable = getattr(client, self._list_function)
        return [callable(**self._list_parameters)]
