from aws_cdk import (
    aws_codepipeline as cp,
    aws_codepipeline_actions as cp_actions,
    aws_codebuild as cb,
    aws_codedeploy as cd,
    aws_s3 as s3,
    aws_secretsmanager as sm,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_cloudformation as cfn,
    core
) 

class CodePipelineProdStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        artifact_bucket = s3.Bucket(self, "artifactbucket",
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        application_name = cd.ServerApplication.from_server_application_name(
            self,'appname',
            server_application_name="Clientell"
        )
        dep_group = cd.ServerDeploymentGroup.from_server_deployment_group_attributes(
            self, 'dep_group',
            application=application_name,
            deployment_group_name="prod"
        )

        
        github_token = core.SecretValue.secrets_manager(
            'stg/clientell/github-token', json_field='github-token'
        )
        
        pipeline = cp.Pipeline(self, "prdpipeline",
            pipeline_name="DeployToProd",
            artifact_bucket=artifact_bucket,
            restart_execution_on_update=False

        )

        sourceOutput = cp.Artifact(artifact_name="source")
        buildOutput = cp.Artifact(artifact_name="output")

        pipeline.add_stage(stage_name='Source',actions=[
            cp_actions.GitHubSourceAction(
                oauth_token=github_token,
                output=sourceOutput,
                repo="clientell-webapp",
                branch="master",
                owner="revstarconsulting",
                action_name="GitHubSource"
            )
        ])

        pipeline.add_stage(stage_name='DeployToProduction',actions=[
            cp_actions.CodeDeployServerDeployAction(
                deployment_group=dep_group,
                input=sourceOutput,
                action_name="DeployToProduction"
            )
        ])
        

        artifact_bucket.grant_read_write(pipeline.role)