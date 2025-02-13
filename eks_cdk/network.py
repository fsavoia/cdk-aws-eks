# I will use the default option from Cluster construct
# vpc (Optional[IVpc]) – The VPC where your ECS instances will be running or
# your ENIs will be deployed. Default: - creates a new VPC with two AZs
#
#
from aws_cdk import CfnOutput, Stack, Tags
from aws_cdk import aws_ec2 as ec2
from constructs import Construct


class VpcStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc_cidr = self.node.try_get_context("vpc_cidr")

        vpc = ec2.Vpc(
            self,
            "MyVpc",
            ip_addresses=ec2.IpAddresses.cidr(vpc_cidr),
            max_azs=3,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                # private subnet is commented to avoid free tier costs
                # with NAT Gateway
                #
                # ec2.SubnetConfiguration(
                #     name="Private",
                #     subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                #     cidr_mask=24,
                # ),
            ],
        )

        Tags.of(vpc).add("Name", "EKSVpC")

        for i, subnet in enumerate(vpc.public_subnets, start=1):
            Tags.of(subnet).add("Name", f"eks-public-subnet-{i}")

        CfnOutput(self, "VpcId", value=vpc.vpc_id, export_name="VpcId")
