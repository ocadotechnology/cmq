from cmq.aws.aws import AWSResource

class region(AWSResource):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = "account"
        self._resource = "region"
        self._list_function = "list_regions"
        self._list_key = "Regions"
        self._list_parameters = {"RegionOptStatusContains": ["ENABLED", "ENABLED_BY_DEFAULT"]}

    def __call__(self, regions: list[str] = [], **kwargs) -> "region":
        self._regions = regions
        self._list_parameters = kwargs
        return self

    def get(self, context: dict) -> list[dict]:
        if self._regions:
            return [{"RegionName": region} for region in self._regions]
        return super().get(context)

    def traverse(self, context: dict) -> None:
        for resource in self.bar(context, self.get(context), desc=f"{self._desc} traverse"):
            aws_region = resource.get("RegionName")
            aws_session = context.get("aws_session")
            aws_session._session.set_config_variable('region', aws_region)
            context.update({
                "aws_region": aws_region,
                "aws_session": aws_session,
                self._desc: resource
            })
            self._traverse(context)
