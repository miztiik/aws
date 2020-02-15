from aws_cdk import (
    aws_codepipeline as cp,
    aws_codepipeline_actions as cp_actions,
    aws_codebuild as cb,
    aws_s3 as s3,
    aws_secretsmanager as sm,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_cloudformation as cfn,
    core
) 

class CodePipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, artifactbucket,buildlogsbucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #prj_name = self.node.try_get_context("project_name")
        #env_name = self.node.try_get_context("env")

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
            build_spec=cb.BuildSpec.from_object({
                'version': '0.2',
                'phases': {
                    'install': {
                        'commands':[
                            'echo "----INSTALL PHASE----" ',
                            'npm install -g serverless',
                            'npm install --save-dev serverless-sam',
                            'pip install awscli'
                        ]
                    },
                    'build': {
                        'commands':[
                            'echo "-----BUILD PHASE------"',
                            'serverless sam export --output sam-template.yaml',
                            'aws cloudformation package --template-file sam-template.yaml --s3-bucket $BUCKET --output-template packaged-template.yaml'
                        ]
                            
                    },
                    'post_build':{
                        'commands': [
                            'echo "-----POST BUILD PHASE-----" ',
                            'echo "SAM packaging completed on `date` "'
                        ]
                    }

                },
                'artifacts': {
                    'files': ['packaged-template.yaml'],
                    'discard-paths': 'yes',
                },
                'cache': {
                    'paths': ['/root/.cache/pip'],
                }
            })
        )
        
        
        github_token = core.SecretValue.secrets_manager(
            'dev/msa/github-token', json_field='github-token'
        )

        pipeline = cp.Pipeline(self, "pipeline",
            pipeline_name="DeployLambdaFunctions",
            artifact_bucket=buildlogs_bucket,
            restart_execution_on_update=True,
        )

        sourceOutput = cp.Artifact(artifact_name="source")
        buildOutput = cp.Artifact(artifact_name="output")
        cfn_outpt = cp.Artifact()

        pipeline.add_stage(stage_name='Source',actions=[
            cp_actions.GitHubSourceAction(
                oauth_token=github_token,
                output=sourceOutput,
                repo="serverless",
                branch="master",
                owner="nixsupport",
                action_name="GitHubSource"
            )
        ])

        pipeline.add_stage(stage_name='Build',actions=[
            cp_actions.CodeBuildAction(
                action_name="TransformTemplate",
                input=sourceOutput,
                project=build_project,
                outputs=[buildOutput],
                type=cp_actions.CodeBuildActionType.BUILD
            )
        ])

        pipeline.add_stage(stage_name='DeployToDev', actions=[
            cp_actions.CloudFormationCreateReplaceChangeSetAction(
                action_name='CreateChangeSet',
                admin_permissions=True,
                change_set_name='serverless-changeset-development',
                stack_name='ServerlessPipelineDev',
                template_path=cp.ArtifactPath(
                    buildOutput,
                    file_name='packaged-template.yaml'
                ),
                capabilities=[cfn.CloudFormationCapabilities.ANONYMOUS_IAM],
                run_order=1
            ),
            cp_actions.CloudFormationExecuteChangeSetAction(
                action_name='ExecuteChangeSet',
                change_set_name='serverless-changeset-development',
                stack_name='ServerlessPipelineDev',
                output=cfn_outpt,
                run_order=2
            )
        ])
            
        artifact_bucket.grant_read_write(pipeline.role)

        
        
        
            