from aws_cdk import (
    aws_apigateway as apigw,
    core
) 

class APIStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        api_gateway = apigw.RestApi(self,'restapi',
            endpoint_types=[apigw.EndpointType.REGIONAL],
            minimum_compression_size=1024,
            binary_media_types=["multipart/form-data"],
            rest_api_name=prj_name+'-apigateway',
            
        )
        apigw.Method(self,'method1',
            http_method="POST",
            resource=api_gateway
        )

        #TODO
        #domain name

        
        
        
            