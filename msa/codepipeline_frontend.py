from aws_cdk import (
    aws_codepipeline as cp,
    aws_codepipeline_actions as cp_actions,
    aws_codebuild as cb,
    aws_s3 as s3,
    aws_secretsmanager as sm,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_cloudformation as cfn,
    aws_cloudfront as cdn,
    core
) 

class CodePipelineFrontendStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, buildlogsbucket, webhostingbucket, distributionid, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #prj_name = self.node.try_get_context("project_name")
        #env_name = self.node.try_get_context("env")

        webhosting_bucket = s3.Bucket.from_bucket_name(self,'webhostingbucket',webhostingbucket)
        buildlogs_bucket = s3.Bucket.from_bucket_name(self,'buildlogsbucket',buildlogsbucket)
        #distribution_id = distributionid
        #distribution_id = cdn.
        #get_build_dev_role = ssm.StringParameter.value_from_lookup(self, 
        #    parameter_name='/dev/codebuild/role'    
        #)

        build_project = cb.PipelineProject(self, 'buildfrontend',
            project_name='Build',
            description='package react app',
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.STANDARD_3_0,
                environment_variables={
                    #'BUCKET': cb.BuildEnvironmentVariable(value=webhosting_bucket.bucket_name),
                    'env': cb.BuildEnvironmentVariable(value='dev'),
                    'distributionid': cb.BuildEnvironmentVariable(value=distributionid)
                }
            ),
            cache=cb.Cache.bucket(buildlogs_bucket,prefix='codebuild-cache'),
            build_spec=cb.BuildSpec.from_object({
                'version': '0.2',
                'phases': {
                    'pre_build': {
                        'commands': [
                            'echo "-----PRE BUILD PHASE-----" ',
                            'npm install',
                            'pip install awscli'
                        ]
                    },
                    'build': {
                        'commands': [
                            'echo "----BUILD PHASE----" ',
                            'npm run build'
                        ]
                    },
                    'post_build': {
                        'commands' : [
                            'echo "-----POST BUILD PHASE----- "',
                            'aws cloudfront create-invalidation --distribution-id $distributionid --paths "/*" '
                        ]
                    }
                },
                'artifacts': {
                    'files': [
                        '**/*'
                    ]
                },
                'base-directory': 'build',
                'cache': {
                    'paths': ['/root/.cache/pip'],
                }

            })
        )
        
        github_token = core.SecretValue.secrets_manager(
            'dev/msa/github-token', json_field='github-token'
        )
        
        pipeline = cp.Pipeline(self, "frontend-pipeline",
            pipeline_name="DeployFrontend",
            artifact_bucket=buildlogs_bucket,
            restart_execution_on_update=True
        )

        sourceOutput = cp.Artifact(artifact_name="source")
        buildOutput = cp.Artifact(artifact_name="output")
        deploydevOutput = cp.Artifact(artifact_name="deploydev")
        cfn_outpt = cp.Artifact()

        pipeline.add_stage(stage_name='Source',actions=[
            cp_actions.GitHubSourceAction(
                oauth_token=github_token,
                output=sourceOutput,
                repo="MSATechnology-ReactJS",
                branch="master",
                owner="revstarconsulting",
                action_name="GitHubSource"
            )
        ])

        pipeline.add_stage(stage_name='Build',actions=[
            cp_actions.CodeBuildAction(
                action_name="Build",
                input=sourceOutput,
                project=build_project,
                outputs=[buildOutput],
                type=cp_actions.CodeBuildActionType.BUILD
            )
        ])
        
        pipeline.add_stage(stage_name='Deploy', actions=[
            cp_actions.S3DeployAction(
                bucket=webhosting_bucket,
                input=buildOutput,
                action_name='Deploy',
                extract=True
            )
        ])

        buildlogs_bucket.grant_read_write(pipeline.role)

        
        
        
            