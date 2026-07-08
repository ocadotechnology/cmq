import boto3
import csv
import io

from moto import mock_aws
from mock_resources import MockSession


def create_fake_kinesis(region, name, team=None):
    client = boto3.session.Session(region_name=region).client("kinesis")
    client.create_stream(StreamName=name, ShardCount=1)
    if team:
        stream_arn = client.describe_stream(StreamName=name)["StreamDescription"]["StreamARN"]
        client.add_tags_to_stream(StreamARN=stream_arn, Tags={"Team": team})


def create_fake_dynamodb(region, name, team):
    client = boto3.session.Session(region_name=region).client("dynamodb")
    client.create_table(
        TableName=name,
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        },
        Tags=[
            {"Key": "Team", "Value": team},
        ],
    )


@mock_aws()
def test_resources_list():

    create_fake_kinesis("us-east-1", "dev-stream")
    create_fake_kinesis("eu-west-1", "sit-stream")
    create_fake_kinesis("us-east-2", "rte-stream")
    create_fake_kinesis("ca-central-1", "prd-stream")

    session = MockSession(None)
    resources = session().kinesis().list()

    assert isinstance(resources, list)
    assert len(resources) == 3
    assert all(key in resources[0].keys() for key in ['StreamName', 'StreamARN', 'StreamStatus', 'StreamModeDetails', 'StreamCreationTimestamp'])


@mock_aws()
def test_resources_dict():

    create_fake_kinesis("us-east-1", "dev-stream")
    create_fake_kinesis("eu-west-1", "sit-stream")
    create_fake_kinesis("us-east-2", "rte-stream")
    create_fake_kinesis("ca-central-1", "prd-stream")

    session = MockSession(None)
    resources = session().kinesis().dict()

    assert isinstance(resources, dict)
    assert len(resources) == 3


@mock_aws()
def test_resources_attr():

    create_fake_kinesis("us-east-1", "dev-stream")
    create_fake_kinesis("eu-west-1", "sit-stream")
    create_fake_kinesis("us-east-2", "rte-stream")
    create_fake_kinesis("ca-central-1", "prd-stream")

    session = MockSession(None)
    resource = session().kinesis().attr("StreamName").list()[0]

    assert isinstance(resource, dict)
    assert resource.keys() == {"StreamName",}


@mock_aws()
def test_resources_filter():

    create_fake_kinesis("us-east-1", "dev-stream")
    create_fake_kinesis("eu-west-1", "sit-stream")
    create_fake_kinesis("us-east-2", "rte-stream")
    create_fake_kinesis("ca-central-1", "prd-stream")

    session = MockSession(None)
    resources = session().kinesis().eq("StreamName", "dev-stream").list()

    assert isinstance(resources, list)
    assert len(resources) == 1
    assert resources[0]["StreamName"] == "dev-stream"


@mock_aws()
def test_resources_sort():

    create_fake_kinesis("us-east-1", "dev-stream")
    create_fake_kinesis("eu-west-1", "sit-stream")
    create_fake_kinesis("ca-central-1", "prd-stream")

    session = MockSession(None)
    resources = session().kinesis().list(sort="StreamName")

    assert [r["StreamName"] for r in resources] == ["dev-stream", "prd-stream", "sit-stream"]


@mock_aws()
def test_resources_sort_nested_key():

    create_fake_kinesis("us-east-1", "dev-stream", team="teamC")
    create_fake_kinesis("eu-west-1", "sit-stream", team="teamA")
    create_fake_kinesis("ca-central-1", "prd-stream", team="teamB")

    session = MockSession(None)
    resources = session().kinesis().tags().list(sort="Tags.Team")

    assert [r["Tags"]["Team"] for r in resources] == ["teamA", "teamB", "teamC"]


@mock_aws()
def test_resources_csv_sort():

    create_fake_kinesis("us-east-1", "dev-stream")
    create_fake_kinesis("eu-west-1", "sit-stream")
    create_fake_kinesis("ca-central-1", "prd-stream")

    session = MockSession(None)
    result = session().kinesis().attr("StreamName").csv(sort="StreamName")

    rows = list(csv.reader(io.StringIO(result)))
    header, data_rows = rows[0], rows[1:]

    assert header == ["StreamName", "session"]
    assert [row[0] for row in data_rows] == ["dev-stream", "prd-stream", "sit-stream"]


@mock_aws()
def test_pipeline_operation_order():

    create_fake_dynamodb("us-east-1", "teamA", "teamA")
    create_fake_dynamodb("us-east-1", "teamB", "teamB")
    create_fake_dynamodb("us-east-1", "teamC", "teamC")
    create_fake_dynamodb("us-east-1", "teamD", "teamD")
    create_fake_dynamodb("us-east-1", "teamE", "teamE")

    session = MockSession(None)
    resources = (
        session().dynamodb()
        .calculate("TableNameUpper", lambda x: x["resource"].upper())
        .eq("TableNameUpper", "TEAME")
        .describe()
        .calculate("TableStatus", lambda x: x["Describe"]["Table"]["TableStatus"])
        .attr("resource", "TableNameUpper", "TableStatus")
        .list()
    )

    assert len(resources) == 1
    assert resources[0]["TableNameUpper"] == "TEAME"
    assert resources[0]["TableStatus"] == "ACTIVE"
