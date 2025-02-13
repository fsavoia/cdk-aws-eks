#!/usr/bin/env python3
import os

from aws_cdk import App, Environment, Tags

from eks_cdk.cr_lambda import CustomResourceStack
from eks_cdk.eks import EksClusterStack
from eks_cdk.helpers import get_current_environment
from eks_cdk.ssm import SsmStack

app = App()

default_region = app.node.try_get_context("region")
region = os.environ.get("CDK_DEFAULT_REGION") or default_region
environment = get_current_environment(scope=app)
project = app.node.try_get_context("project")

env = Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=region,
)

Tags.of(app).add("Environment", environment)
Tags.of(app).add("Project", project)

ssm_stack = SsmStack(app, "SsmStack")
custom_resource_stack = CustomResourceStack(app, "CustomResourceStack")
eks_cluster_stack = EksClusterStack(app, "EksClusterStack")

custom_resource_stack.add_dependency(ssm_stack)
eks_cluster_stack.add_dependency(custom_resource_stack)

app.synth()
