import pytest

from assets.custom_resource.app import handler


def test_handler_create_update_dev_success(
    dev_ssm_parameter, ssm_parameter_name, monkeypatch
):
    """Test handler for Create/Update request in development environment."""
    monkeypatch.setenv("SSM_PARAM_NAME", ssm_parameter_name)

    event = {"RequestType": "Create"}
    context = {}

    response = handler(event, context)

    assert response["Status"] == "SUCCESS"
    assert response["Data"]["controller.replicaCount"] == 1


def test_handler_create_update_stg_success(
    stg_ssm_parameter, ssm_parameter_name, monkeypatch
):
    """Test handler for Create/Update request in staging environment."""
    monkeypatch.setenv("SSM_PARAM_NAME", ssm_parameter_name)

    event = {"RequestType": "Create"}
    context = {}

    response = handler(event, context)

    assert response["Status"] == "SUCCESS"
    assert response["Data"]["controller.replicaCount"] == 2


def test_handler_create_update_prod_success(
    prod_ssm_parameter, ssm_parameter_name, monkeypatch
):
    """Test handler for Create/Update request in production environment."""
    monkeypatch.setenv("SSM_PARAM_NAME", ssm_parameter_name)

    event = {"RequestType": "Create"}
    context = {}

    response = handler(event, context)

    assert response["Status"] == "SUCCESS"
    assert response["Data"]["controller.replicaCount"] == 2


def test_handler_unknown_environment(ssm, ssm_parameter_name, monkeypatch):
    """Test handler for Create request with unknown environment."""
    ssm.put_parameter(Name=ssm_parameter_name, Value="unknown_env", Type="String")
    monkeypatch.setenv("SSM_PARAM_NAME", ssm_parameter_name)

    event = {"RequestType": "Create"}
    context = {}

    response = handler(event, context)

    assert response["Status"] == "FAILED"
    assert "Unknown environment" in response["Reason"]


def test_handler_update_success(prod_ssm_parameter, ssm_parameter_name, monkeypatch):
    """Test handler for Update request in production environment."""
    monkeypatch.setenv("SSM_PARAM_NAME", ssm_parameter_name)

    event = {"RequestType": "Update"}
    context = {}

    response = handler(event, context)

    assert response["Status"] == "SUCCESS"
    assert response["Data"]["controller.replicaCount"] == 2
