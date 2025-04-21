import json
from cmq.aws.session.profile import profile

resources = profile() \
        .log(logGroupNamePrefix="/aws/lambda/send_email") \
        .stream(logStreamNamePrefix="2024/10/16") \
        .event() \
        .dict()

with open("lambda_logs.json", "w") as f:
    json.dump(resources, f, indent=4, default=str)
