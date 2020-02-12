from aws_cdk import (
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_kms as kms,
    core
) 

class RDSStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc,sg, kmskey, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rdskey = kms.Key.from_key_arn(self,"rdskey",
            key_arn=kmskey
        )

        db_mysql = rds.DatabaseCluster(self,"Dev_MySQL",
            default_database_name="msadev",
            engine=rds.DatabaseClusterEngine.AURORA_MYSQL,
            engine_version="5.7.12",
            master_user=rds.Login(username="admin"),
            instance_props=rds.InstanceProps(
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
                instance_type=ec2.InstanceType(instance_type_identifier="t3.medium")
            ),
            instances=1,
            parameter_group=rds.ClusterParameterGroup.from_parameter_group_name(
                self,"paramter-group-msadev",
                parameter_group_name="default.aurora-mysql5.7"
            ),
            kms_key=rdskey

        )
        sgId = ec2.SecurityGroup.from_security_group_id(self,"sgid",sg)
        db_mysql.connections.allow_default_port_from(sgId,"Access from Bastion")

        
        
        
            