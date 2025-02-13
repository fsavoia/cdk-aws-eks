from aws_cdk import CfnOutput, Fn, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_eks as eks
from aws_cdk import aws_iam as iam
from aws_cdk.lambda_layer_kubectl import KubectlLayer
from constructs import Construct


class EksClusterStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        kubectl_layer = KubectlLayer(self, "KubectlLayer")

        eks_master_role = iam.Role(
            self,
            "EksMasterRole",
            role_name="EksAdminRole",
            assumed_by=iam.AccountRootPrincipal(),
        )

        cluster = eks.Cluster(
            self,
            "EksCluster",
            cluster_name="CDK_EKS",
            default_capacity=2,
            default_capacity_instance=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM
            ),
            masters_role=eks_master_role,
            kubectl_layer=kubectl_layer,
            version=eks.KubernetesVersion.V1_29,
        )

        helm_values = Fn.import_value("HelmValuesReplicaCount")

        eks.HelmChart(
            self,
            "IngressNginx",
            cluster=cluster,
            chart="ingress-nginx",
            release="ingress-nginx",
            repository="https://kubernetes.github.io/ingress-nginx",
            namespace="ingress-nginx",
            values={"controller": {"replicaCount": helm_values}},
        )

        CfnOutput(self, "ClusterName", value=cluster.cluster_name)
