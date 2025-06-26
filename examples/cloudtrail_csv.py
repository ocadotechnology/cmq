from datetime import datetime, timedelta
from cmq.aws.session.profile import profile

resources = profile() \
            .cloudtrail() \
                .event_source("elasticache.amazonaws.com") \
                .event_time(datetime.now() - timedelta(days=1), datetime.now()) \
            .csv(True)

with open("cloudtrail_csv.csv", "w") as f:
    f.write(resources)
