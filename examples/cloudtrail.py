import json
from cmq.aws.session.profile import profile

resources = profile() \
            .cloudtrail() \
                .event_name("CreateChangeSet") \
                .attr("Username", "EventTime", "Resources") \
                .ends_with("Username", "@company.com") \
            .dict()

with open("cloudtrail.json", "w") as f:
    json.dump(resources, f, indent=4, default=str)
