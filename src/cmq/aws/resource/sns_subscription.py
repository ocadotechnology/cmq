from typing import Any
from cmq.aws.aws import AWSResource


class sns_subscription(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "sns"
        self._resource = "sns_subscriptions"
        self._list_function = "list_subscriptions"

    def get_parameters(self, context: dict) -> dict:
        parameters = self._list_parameters.copy()
        if 'sns_sns' in context:
            self._list_function = "list_subscriptions_by_topic"
            parameters["TopicArn"] = context["sns_sns"]["TopicArn"]
        return parameters
