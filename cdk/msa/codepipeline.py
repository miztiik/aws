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
        
        get_build_dev_role = ssm.StringParameter.value_from_lookup(self, 
            parameter_name='/dev/codebuild/role'    
        )

        build_project = cb.PipelineProject(self,'buildtemplate',
            project_name="DeployToDev",
            description="Package Serverless Project",
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.STANDARD_3_0,
                environment_variables={
                    'BUCKET': cb.BuildEnvironmentVariable(value=artifact_bucket.bucket_name),
                    'env': cb.BuildEnvironmentVariable(value='dev')
                },
            ),
            role=get_build_dev_role,
            cache=cb.Cache.bucket(artifact_bucket,prefix='codebuild-cache'),
            build_spec=cb.BuildSpec.from_object({
                'version': '0.2',
                'phases': {
                    'install': {
                        'commands':[
                            'echo "----INSTALL PHASE----" ',
                            'npm install --silent --no-progress npm -g',
                            'npm install --silent --no-progress serverless -g'
                        ]
                    },
                    'pre_build': {
                        'commands':[
                            'echo "----PRE BUILD PHASE----" ',
                            'npm install --no-progress --silent'
                        ]
                    },
                    'build': {
                        'commands':[
                            'echo "-----BUILD PHASE------"',
                            'serverless deploy --stage $env'
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
                    'files': [
                        'target/**/*',
                        'serverless.yaml'
                    ]
                },
                'cache': {
                    'paths': ['/root/.cache/pip'],
                }
            })
        )

        
        deploy_project = cb.PipelineProject(self,'deploy',
            project_name="DeployFunction",
            description="Deploy Serverless Project",
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.STANDARD_3_0,
                environment_variables={
                    'BUCKET': cb.BuildEnvironmentVariable(value=artifact_bucket.bucket_name),
                    'env': cb.BuildEnvironmentVariable(value='dev')
                },
            ),
            build_spec=cb.BuildSpec.from_object({
                'version': '0.2',
                'phases': {
                    'install': {
                        'commands':[
                            'echo "----INSTALL PHASE----" ',
                            'npm install --no-progress --silent serverless -g'
                        ]
                    },
                    'pre_build': {
                        'commands':[
                            'echo "----PRE BUILD PHASE----" ',
                            'npm install --no-progress --silent -g'
                        ]
                    },
                    'build': {
                        'commands':[
                            'echo "-----BUILD PHASE------"',
                            'serverless deploy --stage $env --package $BUCKET/target/$env'
                        ]
                            
                    }
                }
            })
        )
        
        
        github_token = core.SecretValue.secrets_manager(
            'dev/msa/github-token', json_field='github-token'
        )
        
        pipeline = cp.Pipeline(self, "pipeline",
            pipeline_name="DeployLambdaFunctions",
            artifact_bucket=artifact_bucket,
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
                repo="MSATechnology-NodeJS",
                branch="master",
                owner="revstarconsulting",
                action_name="GitHubSource"
            )
        ])

        pipeline.add_stage(stage_name='DeployToDev',actions=[
            cp_actions.CodeBuildAction(
                action_name="DeployToDev",
                input=sourceOutput,
                project=build_project,
                outputs=[buildOutput],
                #type=cp_actions.CodeBuildActionType.BUILD
            )
        ])

        '''
        pipeline.add_stage(stage_name='DeployDev', actions=[
            cp_actions.CodeBuildAction(
                action_name='DeployDev',
                input=buildOutput,
                project=deploy_project,
                outputs=[deploydevOutput],
                
            )
        ])
        '''
        '''
        pipeline.add_stage(stage_name='DeployToDev', actions=[
            cp_actions.CloudFormationCreateReplaceChangeSetAction(
                action_name='CreateChangeSet',
                admin_permissions=True,
                change_set_name='serverless-changeset-development',
                stack_name='ServerlessPipelineDev',
                template_path=cp.ArtifactPath(
                    buildOutput,
                    file_name='cloudformation-template-update-stack.json'
                ),
                capabilities=[cfn.CloudFormationCapabilities.NAMED_IAM, 
                    cfn.CloudFormationCapabilities.AUTO_EXPAND, 
                    cfn.CloudFormationCapabilities.ANONYMOUS_IAM],
                run_order=1
            ),
            cp_actions.CloudFormationExecuteChangeSetAction(
                action_name='ExecuteChangeSet',
                change_set_name='serverless-changeset-development',
                stack_name='ServerlessPipelineDev',
                output=cfn_outpt,
                run_order=2,
                
            )
        ])
        '''    
        artifact_bucket.grant_read_write(pipeline.role)

        
        
        
            
