import boto3

from moto import mock_aws
from mock_resources import MockSession


def create_fake_kinesis(region, name):
    client = boto3.session.Session(region_name=region).client("kinesis")
    client.create_stream(StreamName=name, ShardCount=1)


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
