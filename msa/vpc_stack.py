from aws_cdk import (
    aws_ec2 as ec2,
    core
) 

class VPCStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        self.vpc = ec2.Vpc(self,'devVPC',
            cidr="172.32.0.0/16",
            max_azs=2,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            subnet_configuration=[ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.PUBLIC,
                name="Dev-Public",
                cidr_mask=24
            ),
            ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.PRIVATE,
                name="Dev-Private",
                cidr_mask=24
            ),
            ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.ISOLATED,
                name="Dev-DB",
                cidr_mask=24
            )
            
            ],
            nat_gateways=2
        )

        #core.CfnOutput(self,'devvpc',
        #    value=self.vpc.vpc_id,
        #    export_name='dev-vpc'
        #)
        
        
        
            