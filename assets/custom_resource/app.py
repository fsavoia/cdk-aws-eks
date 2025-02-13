import logging
import os

import boto3

ssm = boto3.client("ssm")

REPLICA_MAP = {
    "development": 1,
    "staging": 2,
    "production": 2,
}

PARAMETER_NAME = os.environ.get("SSM_PARAM_NAME", "/platform/account/env")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    request_type = event.get("RequestType")
    if request_type in ["Create", "Update"]:
        try:
            response = ssm.get_parameter(Name=PARAMETER_NAME)
            environment = response["Parameter"]["Value"]

            replica_count = REPLICA_MAP.get(environment)

            if replica_count is None:
                raise ValueError(f"Unknown environment: {environment}")

            response = {
                "Status": "SUCCESS",
                "Data": {"controller.replicaCount": replica_count},
            }

            logger.info(response)

            return response
        except Exception as e:
            logger.error("Error retrieving parameter: %s", e)
            return {"Status": "FAILED", "Reason": str(e)}
    elif request_type == "Delete":
        response = {"Status": "SUCCESS", "Data": {}}
        logger.info(response)

        return response
    else:
        response = {
            "Status": "FAILED",
            "Reason": f"Unsupported request type: {request_type}",
        }
        logger.error(response)

        return response
