#!/usr/bin/env python3

from aws_cdk import core

from msa.cdn_stack import CDNStack
from msa.s3_stack import S3Stack
from msa.vpc_stack import VPCStack
from msa.rds_stack import RDSStack
from msa.ec2_stack import EC2Stack
from msa.kms_stack import KMSStack
from msa.redis_stack import RedisStack
#from msa.apigateway_stack import APIStack
from msa.codepipeline import CodePipelineStack
from msa.cognito import CognitoStack
from msa.codepipeline_frontend import CodePipelineFrontendStack
app = core.App()

s3_stack = S3Stack(app, "s3")
cdn_stack = CDNStack(app, "cdn", s3bucket=core.Fn.import_value('webhosting-bucket'))
vpc_stack = VPCStack(app, "vpc")
kms_stack = KMSStack(app, "kms")
redis_stack = RedisStack(app, "redis", vpc=vpc_stack.vpc)
ec2_stack = EC2Stack(app, "ec2", vpc=vpc_stack.vpc)
rds_stack = RDSStack(app, "rds", vpc=vpc_stack.vpc, sg=ec2_stack.sg.security_group_id,redissg=core.Fn.import_value('redis-sg-export'),kmskey=kms_stack.kms_rds.key_arn)
#api_stack = APIStack(app, "apigw")
codepipeline_stack = CodePipelineStack(app, "codepipeline", artifactbucket=core.Fn.import_value('lambda-bucket'),
    buildlogsbucket=core.Fn.import_value('build-logs-bucket'),
    env={'account':'748496058110', 'region': 'us-east-1'})

codepipeline_frontend_stack = CodePipelineFrontendStack(app, "codepipeline-frontend", buildlogsbucket=core.Fn.import_value('build-logs-bucket'), 
        webhostingbucket=core.Fn.import_value('webhosting-bucket'),
        distributionid=core.Fn.import_value('distribution-id'))

#cognito_stack = CognitoStack(app, "cognito")

app.synth()
