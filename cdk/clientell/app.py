#!/usr/bin/env python3

from aws_cdk import core

from codepipeline import CodePipelineStack
from codepipeline_prod import CodePipelineProdStack

app = core.App()

codepipeline_stack = CodePipelineStack(app, "codepipeline")
codepipeline_prod_stack = CodePipelineProdStack(app, "codepipelineprod")

app.synth()
