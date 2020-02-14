from aws_cdk import (
    aws_codepipeline as cp,
    aws_codepipeline_actions as cp_actions,
    aws_codebuild as cb,
    aws_s3 as s3,
    aws_secretsmanager as sm,
    aws_iam as iam,
    core
) 

class CodePipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, artifactbucket,buildlogsbucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #prj_name = self.node.try_get_context("project_name")
        #env_name = self.node.try_get_context("env")

        sourceOutput = cp.Artifact(artifact_name="source")
        #buildOutput = cp.Artifact(artifact_name="output")
        
        artifact_bucket = s3.Bucket.from_bucket_name(self,'artifactbucket',artifactbucket)
        buildlogs_bucket = s3.Bucket.from_bucket_name(self,'buildlogsbucket',buildlogsbucket)

        build_project = cb.PipelineProject(self,'buildtemplate',
            project_name="BuildFunction",
            description="Transform Serverless Framework template to CFN template",
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.STANDARD_3_0,
                environment_variables={
                    'BUCKET': cb.BuildEnvironmentVariable(value=artifact_bucket.bucket_name)
                },
            ),
            cache=cb.Cache.bucket(artifact_bucket,prefix='codebuild-cache'),
            build_spec=cb.BuildSpec.from_source_filename(
                filename='buildspec.yaml'
            )
        )
        oauthToken=core.SecretValue.plain_text('oauth_token')

        pipeline = cp.Pipeline(self, "pipeline",
            pipeline_name="DeployLambdaFunctions",
            artifact_bucket=buildlogs_bucket,
            stages=[
                cp.StageProps(
                    stage_name='Source',
                    actions=[
                        cp_actions.GitHubSourceAction(
                            oauth_token=oauthToken,
                            output=sourceOutput,
                            repo="serverless",
                            branch="master",
                            owner="nixsupport",
                            action_name="GitHubSource",
                            run_order=1
                        )
                    ]
                ),
                cp.StageProps(
                    stage_name="Build",
                    actions=[
                        cp_actions.CodeBuildAction(
                            action_name="TransformTemplate",
                            input=sourceOutput,
                            project=build_project,
                            run_order=1

                        )
                    ]
                )
            ]
        )
        artifact_bucket.grant_read_write(pipeline.role)
        
        #TODO
        #domain name

        
        
        
            