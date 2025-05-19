import json
from collections import defaultdict
from functools import partial
from cmq.aws.session.profile import profile


policies = defaultdict(list)

def action(policies, context):
    session = context["aws_session"]
    client = session.client("iam")
    resource = context["resource-groups_resource-group"]
    results = client.get_paginator("list_entities_for_policy") \
                    .paginate(PolicyArn=resource["ResourceArn"]) \
                    .build_full_result()
    entities = results["PolicyGroups"] + results["PolicyRoles"] + results["PolicyUsers"]
    for entity in entities:
        resource_name = entity.get("GroupName") or entity.get("RoleName") or entity.get("UserName")
        policies[resource_name].append(resource["ResourceArn"])


profile() \
    .resource_group() \
    .search(["AWS::IAM::ManagedPolicy"], appId="admin") \
    .do(partial(action, policies))


with open("policies.json", "w") as f:
    f.write(json.dumps(policies, indent=2))
