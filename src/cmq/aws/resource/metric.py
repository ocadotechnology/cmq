from datetime import datetime, timedelta
from cmq.aws.aws import AWSResource
from matplotlib import pyplot as plt


class metric(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "cloudwatch"
        self._resource = "metric"
        self._list_function = "get_metric_data"
        self._list_key = "MetricDataResults"

    def statistic(self, statistic: str, namespace: str, metric_name: str,
            dimensions: dict = {},
            period: int = 60*60, unit: str = "Count",
            start_time: datetime = None, end_time: datetime = None) -> 'metric':
        # Set default parameter values
        start_time = start_time or datetime.today() - timedelta(days=90)
        end_time = end_time or datetime.today()

        self._list_parameters = {
            "MetricDataQueries": [{
                "Id": f"CMQ_{metric_name}",
                "MetricStat": {
                    "Metric": {
                        "Namespace": namespace,
                        "MetricName": metric_name,
                        "Dimensions": [
                            {"Name": k, "Value": v}
                            for k, v in dimensions.items()
                        ]
                    },
                    "Period": period,
                    "Stat": statistic,
                    "Unit": unit
                },
                "Label": unit,
                "ReturnData": True,
            }],
            "StartTime": start_time,
            "EndTime": end_time
        }
        return self

    def max(self, **kwargs) -> 'metric':
        return self.statistic("Maximum", **kwargs)

    def min(self, **kwargs) -> 'metric':
        return self.statistic("Minimum", **kwargs)

    def avg(self, **kwargs) -> 'metric':
        return self.statistic("Average", **kwargs)

    def sum(self, **kwargs) -> 'metric':
        return self.statistic("Sum", **kwargs)

    def plot(self, unit_factor=1) -> None:
        resources = self.dict()
        plt.clf()
        for session, metrics in resources.items():
            for metric in metrics:
                timestamps = metric["Timestamps"]
                values = [value/unit_factor for value in metric["Values"]]
                plt.plot(timestamps, values, label=session)
        plt.title(self._list_parameters["MetricDataQueries"][0]["MetricStat"]["Metric"]["MetricName"])
        plt.legend(loc='best')
        plt.show()