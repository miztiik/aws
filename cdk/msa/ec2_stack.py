from aws_cdk import (
    aws_ec2 as ec2,
    core
)
#import boto3
#session = boto3.Session(profile_name='msa',region_name='us-east-1')
#cf = session.client("cloudformation")
#vpc_id = next(export['Value'] for export in cf.list_exports()['Exports'] if export['Name'] == 'dev-vpc')

key_name = 'bastion'
linux_ami = ec2.AmazonLinuxImage(
        generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
        edition=ec2.AmazonLinuxEdition.STANDARD,
        virtualization=ec2.AmazonLinuxVirt.HVM,
        storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
)

class EC2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        
        self.sg = ec2.SecurityGroup(self,'bastionSG',
            vpc=vpc,
            security_group_name='BastionHostSG',
            description="SG for Public Access",
            allow_all_outbound=True
        )

        self.sg.add_ingress_rule(ec2.Peer.any_ipv4(),ec2.Port.tcp(22),"SSH Access")

        host = ec2.Instance(self, "bastion",
                instance_type=ec2.InstanceType(
                    instance_type_identifier="t2.micro"),
                instance_name="bastion",
                machine_image=linux_ami,
                vpc=vpc,
                key_name=key_name,
                vpc_subnets=ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                security_group=self.sg

            )
        
        #host.connections.allow_from_any_ipv4(
        #    ec2.Port.tcp(22),"SSH Access"
        #)
        core.CfnOutput(self,'bastionhost',
            value=self.sg.security_group_id
        )
        
        
            