from aws_cdk import CfnOutput, Stack
from aws_cdk import aws_ssm as ssm
from constructs import Construct

from .helpers import get_current_environment


class SsmStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ssm_param_value = get_current_environment(scope=self)

        ssm_param = ssm.StringParameter(
            self,
            "EnvParameter",
            parameter_name="/platform/account/env",
            string_value=ssm_param_value,
        )

        CfnOutput(
            self,
            "SSMParameterNameOutput",
            value=ssm_param.parameter_name,
            export_name="SSMParameterEnvName",
        )
