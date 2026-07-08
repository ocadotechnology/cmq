from cmq.aws.session.profile import profile

resources = profile() \
            .function() \
                .tags() \
                .attr("FunctionArn", "FunctionName", "Runtime", "Tags") \
            .csv(True)

with open("lambdas.csv", "w") as f:
    f.write(resources)
