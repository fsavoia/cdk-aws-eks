import os

import boto3
import pytest
from moto import mock_aws


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def ssm(aws_credentials):
    """
    Return a mocked ssm client
    """
    with mock_aws():
        yield boto3.client("ssm", region_name="us-east-1")


@pytest.fixture
def ssm_parameter_name():
    """Return the SSM parameter name."""
    return "/platform/account/env"


@pytest.fixture
def dev_ssm_parameter(ssm, ssm_parameter_name):
    """Create a development SSM parameter."""
    ssm.put_parameter(Name=ssm_parameter_name, Value="development", Type="String")


@pytest.fixture
def stg_ssm_parameter(ssm, ssm_parameter_name):
    """Create a staging SSM parameter."""
    ssm.put_parameter(Name=ssm_parameter_name, Value="staging", Type="String")


@pytest.fixture
def prod_ssm_parameter(ssm, ssm_parameter_name):
    """Create a production SSM parameter."""
    ssm.put_parameter(Name=ssm_parameter_name, Value="production", Type="String")
