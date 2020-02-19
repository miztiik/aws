Solutions deployed using CloudFormation templates.

cdk
  \
   - msa
       \
       - cdn_stack.py  
       - codepipeline.py
       - ec2_stack.py
       - kms_stack.py
       - rds_stack.py
       - s3_stack.py
       - vpc_stack.py
   - app.py

solutions
   \
   - detect-manual-policy-changes.yaml  #Revert any change made in IAM policies manually. Changes can only be made via CloudFormation
   - detect-manual-role-changes.yaml    #Revert any policy attached manually to IAM roles. Changes can only be made via CloudFormation
   - dlm-recovery.yaml                  #DR process using DLM, StepFunctions and Lambda
   - etlworkflow.yaml                   #Provision ETL Workflow using EMR, Step Functions, Lambda
   - firewallfailover.yaml              #Switch from primary to seconday firewall in case primary goes down and vice-versa
   - guardduty-remediation.yaml         #Auto remediation of GuardDuty findings.
    
