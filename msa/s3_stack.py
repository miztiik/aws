from aws_cdk import (
    aws_s3 as s3,
    core
) 

class S3Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")
        
        #Lambda packages
        lambda_bucket=s3.Bucket(self, "lambda-packages",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            bucket_name=prj_name+'-'+env_name+'-lambda-deploy-packages',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            )

        )
        
        core.CfnOutput(self,'s3-lambda-export',
            value=lambda_bucket.bucket_name,
            export_name='lambda-bucket'
        )

        #images
        images_bucket=s3.Bucket(self, "images",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            bucket_name=prj_name+'-'+env_name+'-images',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            )

        )

        core.CfnOutput(self,'s3-images-export',
            value=images_bucket.bucket_name,
            export_name='images-bucket'
        )

        #AccessLogs
        accesslogs_bucket=s3.Bucket(self, "accesslogs",
            #access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            bucket_name=prj_name+'-'+env_name+'-accesslogs',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            )

        )

        core.CfnOutput(self,'s3-accesslogs-export',
            value=accesslogs_bucket.bucket_name,
            export_name='accesslogs-bucket'
        )

        #website hosting
        webhosting_bucket = s3.Bucket(self, "webhosting-bucket",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            bucket_name=prj_name+'-'+env_name+'-website-hosting',
            server_access_logs_bucket=accesslogs_bucket,
            server_access_logs_prefix="logs/",
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            )
            
        )

        core.CfnOutput(self,'s3-website-export',
            value=webhosting_bucket.bucket_name,
            export_name='webhosting-bucket'
        )

        #Frontend
        frontend_bucket=s3.Bucket(self, "frontend",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            bucket_name=prj_name+'-'+env_name+'-frontend',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            )

        )

        core.CfnOutput(self,'s3-frontend-export',
            value=frontend_bucket.bucket_name,
            export_name='frontend-bucket'
        )

        #Admin
        admin_bucket=s3.Bucket(self, "admin",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            bucket_name=prj_name+'-'+env_name+'-admin',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            )
        )

        core.CfnOutput(self,'s3-admin-export',
            value=admin_bucket.bucket_name,
            export_name='admin-bucket'
        )
        
        #Build Logs
        build_logs_bucket=s3.Bucket(self, "build-logs",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            bucket_name=prj_name+'-'+env_name+'-build-logs',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
            removal_policy=core.RemovalPolicy.DESTROY

        )

        core.CfnOutput(self,'s3-build-logs-export',
            value=build_logs_bucket.bucket_name,
            export_name='build-logs-bucket'
        )

        #FrontEnd Artifacts
        frontend_artifacts_bucket=s3.Bucket(self, "frontend-artifacts",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            bucket_name=prj_name+'-'+env_name+'-frontend-artifacts',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
            removal_policy=core.RemovalPolicy.DESTROY

        )

        core.CfnOutput(self,'s3-frontend-artifacts-export',
            value=frontend_artifacts_bucket.bucket_name,
            export_name='frontend-artifacts-bucket'
        )

        #Admin Artifacts
        admin_artifacts_bucket=s3.Bucket(self, "admin-artifacts",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            bucket_name=prj_name+'-'+env_name+'-admin-artifacts',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
            removal_policy=core.RemovalPolicy.DESTROY

        )

        core.CfnOutput(self,'s3-admin-artifacts-export',
            value=admin_artifacts_bucket.bucket_name,
            export_name='admin-artifacts-bucket'
        )

        #CloudTrail Logs
        cloudtrail_bucket=s3.Bucket(self, "cloudtrail-logs",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            bucket_name=prj_name+'-'+env_name+'-cloudtrail-logs',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            )

        )

        core.CfnOutput(self,'s3-cloudtrail-export',
            value=cloudtrail_bucket.bucket_name,
            export_name='cloudtrail-bucket'
        )
        

        

        

            