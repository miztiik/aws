#!/usr/bin/env python3

from aws_cdk import core

from msa.s3_stack import S3Stack


app = core.App()
S3Stack(app, "s3")

app.synth()
