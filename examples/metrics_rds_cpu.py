from cmq.aws.session.profile import profile

profile() \
  .rds() \
    .tags() \
    .eq("Tags.appId", "webserver") \
  .plot(statistic="Maximum", metric_name="CPUUtilization", unit="Percent")
