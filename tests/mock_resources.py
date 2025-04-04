import boto3
from typing import Any
from cmq.base import Session
from cmq.aws.aws import AWSResource


class MockSession(Session):

    def get_session_context(self, account: dict) -> dict:
        return {
            "session_resource": account,
            "session_name": account["name"],
            "aws_region": account["region"],
            "aws_account": account["id"],
            "aws_session": boto3.Session(region_name=account["region"]),
        }

    def get_sessions(self) -> list:
        return [
            {
                "name": "dev-account",
                "region": "us-east-1",
                "id": "111111111111",
            },
            {
                "name": "sit-account",
                "region": "eu-west-1",
                "id": "222222222222",
            },
            {
                "name": "prd-account",
                "region": "ca-central-1",
                "id": "333333333333",
            },
        ]

    def _get_pages(self, context):
        return [[1,2,3], [4,5,6]]

    def get_paged_results(self, page):
        return page

    def _list(self, results, context) -> None:
        results.append(context["session_resource"])

    def _dict(self, results, context) -> None:
        account = context["session_resource"]
        results[account["id"]] = account

    def kinesis(self) -> AWSResource:
        return MockResource(self)


class MockResource(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "kinesis"
        self._resource = "kinesis"
        self._list_function = "list_streams"
        self._list_key = "StreamSummaries"

        self._tag_function = "list_tags_for_stream"
        self._tag_function_key = "StreamARN"

        self._metric_namespace = "AWS/Kinesis"
        self._metric_dimension_name = "StreamName"
        self._metric_dimension_resource_key = "StreamName"

    def _get_tag_resource_identifier(self, context: dict[str, Any], resource: dict[str, Any]) -> str:
        return resource["StreamARN"]

