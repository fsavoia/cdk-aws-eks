from aws_cdk import CfnOutput, CustomResource, Fn, Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import custom_resources as cr
from constructs import Construct


class CustomResourceStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ssm_parameter_name = Fn.import_value("SSMParameterEnvName")

        lambda_function = _lambda.Function(
            self,
            "CustomResourceLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="app.handler",
            code=_lambda.Code.from_asset("assets/custom_resource"),
            initial_policy=[
                iam.PolicyStatement(
                    actions=["ssm:GetParameter"],
                    resources=[
                        f"arn:aws:ssm:{self.region}:{self.account}:"
                        f"parameter{ssm_parameter_name}"
                    ],
                )
            ],
        )

        provider = cr.Provider(
            self,
            "CustomResourceProvider",
            on_event_handler=lambda_function,
        )

        my_custom_resource = CustomResource(
            self,
            "MyCustomResource",
            service_token=provider.service_token,
            # I decided to make it dynamic, so in every change we will
            # trigger the lambda
            properties={
                "envparametername": ssm_parameter_name,
            },
        )

        self.helm_values = my_custom_resource.get_att(
            "controller.replicaCount"
        ).to_string()

        CfnOutput(
            self,
            "HelmValuesReplicaCount",
            value=self.helm_values,
            export_name="HelmValuesReplicaCount",
            description="The helm values returned by the custom resource",
        )
