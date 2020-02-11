#!/usr/bin/env python3

from aws_cdk import core

from msa.s3_stack import S3Stack
from msa.another_S3 import testS3


app = core.App()
S3Stack(app, "s3")
testS3(app,"tests3")

app.synth()
