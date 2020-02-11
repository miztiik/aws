from aws_cdk import (
    aws_waf as waf,
    core
) 

class wafStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        #prj_name = self.node.try_get_context("project_name")
        waf.CfnRule()
        
            