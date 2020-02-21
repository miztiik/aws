from aws_cdk import (
    aws_cognito as cognito,
    core
) 

class CognitoStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        
        user_pool = cognito.CfnUserPool(self, 'msa',
            auto_verified_attributes=[
                'email'
            ],
            username_attributes=[
                'email'
            ],
            user_pool_name='msa-user-pool',
            schema=[
                {
                    'attributeDataType': 'String',
                    'name': 'custom:tenant_id',
                    'mutable': True
                },
                {
                    'attributeDataType': 'String',
                    'name': 'role',
                    'mutable': True
                },
                {
                    'attributeDataType': 'String',
                    'name': 'restrictions',
                    'mutable': True
                }
            ]
        
        )

        user_pool_client = cognito.CfnUserPoolClient(self,'pool-client',
            user_pool_id=user_pool.ref,
            client_name='msa-user-client'
        )

        '''
        user_pool = cognito.UserPool(self,'msa',
            sign_in_type= cognito.SignInType.EMAIL,
            auto_verified_attributes= [
                cognito.UserPoolAttribute.EMAIL
            ],
            user_pool_name='msa-dev'
            
        )
        
        user_pool_client = cognito.UserPoolClient(self,'msaclient',
            generate_secret=False,
            user_pool_client_name='msa-client',
            user_pool=user_pool,
        )
        '''


        
        
        
            