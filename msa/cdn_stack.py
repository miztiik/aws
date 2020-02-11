from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cdn,
    core
) 

class CDNStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        #prj_name = self.node.try_get_context("project_name")
        webAclId = self.node.try_get_context("web_acl_id")
        webHostingBucket = s3.Bucket(self, "webhosting-bucket",
            access_control=s3.BucketAccessControl.PRIVATE,
            encryption=s3.BucketEncryption.KMS_MANAGED
        )
        #myBucket = core.Fn.import_value('tests3')
        
        webDistribution = cdn.CloudFrontWebDistribution(self,"webhosting-cdn",
            origin_configs=[cdn.SourceConfiguration(
                behaviors=[cdn.Behavior(is_default_behavior=True)],
                s3_origin_source=cdn.S3OriginConfig(
                    s3_bucket_source=webHostingBucket,
                    origin_access_identity=cdn.OriginAccessIdentity(self,'webhosting-origin')
                )
            )],
            web_acl_id=webAclId
        )
        
        
            