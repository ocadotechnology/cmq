from cmq.aws.aws import AWSResource


class ec2(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "ec2"
        self._resource = "instance"
        self._list_function = "describe_instances"

    def _get_results(self, page) -> list | None:
        instances = []
        reservations = page.get("Reservations", [])
        for reservation in reservations:
            for instance in reservation.get("Instances", []):
                instances.append(instance)
        return instances
