import json
from datetime import datetime, timedelta, timezone
from cmq.aws.aws import AWSResource


class cloudtrail(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "cloudtrail"
        self._resource = "event"
        self._list_function = "lookup_events"
        self._transformers = {"CloudTrailEvent": json.loads}

    def event_name(self, event_name: str) -> "cloudtrail":
        """
        Sets the event name for filtering events.

        Args:
            event_name (str): The event name to filter by.

        Returns:
            cloudtrail: The cloudtrail object for method chaining.
        """
        lookup = self._list_parameters.setdefault("LookupAttributes", [])
        lookup.append({"AttributeKey": "EventName", "AttributeValue": event_name})
        return self

    def event_source(self, event_source: str) -> "cloudtrail":
        """
        Sets the event source for filtering events.

        Args:
            event_source (str): The event source to filter by.

        Returns:
            cloudtrail: The cloudtrail object for method chaining.
        """
        lookup = self._list_parameters.setdefault("LookupAttributes", [])
        lookup.append({"AttributeKey": "EventSource", "AttributeValue": event_source})
        return self

    def resource_name(self, resource_name: str) -> "cloudtrail":
        """
        Sets the resource name for filtering events.

        Args:
            resource_name (str): The resource name to filter by.

        Returns:
            cloudtrail: The cloudtrail object for method chaining.
        """
        lookup = self._list_parameters.setdefault("LookupAttributes", [])
        lookup.append({"AttributeKey": "ResourceName", "AttributeValue": resource_name})
        return self

    def user_name(self, user_name: str) -> "cloudtrail":
        """
        Sets the user name for filtering events.

        Args:
            user_name (str): The user name to filter by.

        Returns:
            cloudtrail: The cloudtrail object for method chaining.
        """
        lookup = self._list_parameters.setdefault("LookupAttributes", [])
        lookup.append({"AttributeKey": "Username", "AttributeValue": user_name})
        return self

    def access_key(self, access_key: str) -> "cloudtrail":
        """
        Sets the access key for filtering events.

        Args:
            access_key (str): The access key to filter by.

        Returns:
            cloudtrail: The cloudtrail object for method chaining.
        """
        lookup = self._list_parameters.setdefault("LookupAttributes", [])
        lookup.append({"AttributeKey": "AccessKeyId", "AttributeValue": access_key})
        return self

    def event_time(self, start_time: datetime, end_time: datetime) -> "cloudtrail":
        """
        Sets the event time range for filtering events.

        Args:
            start_time (datetime): The start time of the event range.
            end_time (datetime): The end time of the event range.

        Returns:
            cloudtrail: The cloudtrail object for method chaining.
        """
        self._list_parameters.update({"StartTime": start_time, "EndTime": end_time})
        return self

    def last(self, **kwargs: dict[str, int]) -> "cloudtrail":
        """
        Sets the number of events to retrieve.

        Args:
            **kwargs: The keyword arguments for the timedelta.

        Returns:
            cloudtrail: The cloudtrail object for method chaining.
        """
        self._list_parameters.update({"StartTime": datetime.now(tz=timezone.utc) - timedelta(**kwargs),
                                      "EndTime": datetime.now(tz=timezone.utc)})
        return self