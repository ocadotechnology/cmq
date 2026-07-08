import json
from cmq.aws.session.profile import profile

resources = profile() \
            .metric() \
                .sum(namespace="AWS/Lambda", metric_name="Invocations") \
            .dict()


with open("metrics_invocations.json", "w") as f:
    json.dump(resources, f, indent=4, default=str)