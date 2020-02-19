from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cdn,
    core
) 

class CDNStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, s3bucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucketName = s3.Bucket.from_bucket_name(self,"s3bucket",s3bucket)
        webAclId = self.node.try_get_context("web_acl_id")

        cdnId = cdn.CloudFrontWebDistribution(self,"webhosting-cdn",
            origin_configs=[cdn.SourceConfiguration(
                behaviors=[
                    cdn.Behavior(is_default_behavior=True)
                    #cdn.Behavior(is_default_behavior=False,path_pattern="/img/")
                ],
                s3_origin_source=cdn.S3OriginConfig(
                    s3_bucket_source=bucketName,
                    origin_access_identity=cdn.OriginAccessIdentity(self,'webhosting-origin'),
                    
                ),
            )],
            web_acl_id=webAclId
        )
        core.CfnOutput(self,'cdnid',
            value=cdnId.distribution_id
        )
        #TODO
        #ACM Cert

        
        
        
            