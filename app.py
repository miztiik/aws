#!/usr/bin/env python3

from aws_cdk import core

from msa.cdn_stack import CDNStack
from msa.s3_stack import S3Stack
from msa.vpc_stack import VPCStack
from msa.rds_stack import RDSStack
from msa.ec2_stack import EC2Stack
from msa.kms_stack import KMSStack
from msa.apigateway_stack import APIStack

app = core.App()

s3_stack = S3Stack(app, "s3")
cdn_stack = CDNStack(app, "cdn", s3bucket=core.Fn.import_value('webhosting-bucket'))
vpc_stack = VPCStack(app, "vpc")
kms_stack = KMSStack(app, "kms")
ec2_stack = EC2Stack(app, "ec2", vpc=vpc_stack.vpc)
rds_stack = RDSStack(app, "rds", vpc=vpc_stack.vpc, sg=ec2_stack.sg.security_group_id,kmskey=kms_stack.kms_rds.key_arn)
#api_stack = APIStack(app, "apigw")

app.synth()
