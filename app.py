#!/usr/bin/env python3

from aws_cdk import core

from msa.cdn_stack import CDNStack

app = core.App()
CDNStack(app, "cdn")

app.synth()
