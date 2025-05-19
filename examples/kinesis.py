import json
from cmq.aws.session.profile import profile

resource = profile().kinesis().attr("StreamName").dict()

with open("kinesis.json", "w") as f:
    json.dump(resource, f, indent=4, default=str)

