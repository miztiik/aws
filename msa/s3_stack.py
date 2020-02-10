from aws_cdk import (
    aws_s3 as s3,
    core
) 

class S3Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        prj_name = self.node.try_get_context("project_name")
        imagesBucket = s3.Bucket(self, "images",
            access_control=s3.BucketAccessControl.PRIVATE,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            bucket_name=prj_name + '-images',

        )
