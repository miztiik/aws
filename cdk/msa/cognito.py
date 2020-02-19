from aws_cdk import (
    aws_cognito as cognito,
    core
) 

class CognitoStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        
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


        
        
        
            