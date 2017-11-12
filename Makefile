# Some defaults
AWS ?= aws
AWS_REGION := us-east-1 # Lambda @ Edge is only available in us-east-1
AWS_PROFILE ?= default

AWS_CMD := $(AWS) --profile $(AWS_PROFILE) --region $(AWS_REGION)

STACK_NAME ?= ue1-s3-basic-auth

TAGS ?= Key=Deployment,Value=cloudfront-basic-auth

# Parameters
PARAMETERS ?= \
	ParameterKey=AuthorizationCredentials,ParameterValue=$(AUTHORIZATION_CREDENTIALS) \
	ParameterKey=OriginBucketName,ParameterValue=$(ORIGIN_BUCKET_NAME) \
	ParameterKey=UpdateTime,ParameterValue="$(shell date)"

create-basic-auth:
	$(AWS_CMD) cloudformation create-stack \
		--stack-name $(STACK_NAME) \
		--tags $(TAGS) \
		--template-body file://stacks/s3-basic-auth.yaml \
		--parameters $(PARAMETERS) \
		--capabilities CAPABILITY_NAMED_IAM

update-basic-auth:
	$(AWS_CMD) cloudformation update-stack \
		--stack-name $(STACK_NAME) \
		--tags $(TAGS) \
		--template-body file://stacks/s3-basic-auth.yaml \
		--parameters $(PARAMETERS) \
		--capabilities CAPABILITY_NAMED_IAM

validate-basic-auth:
	$(AWS_CMD) cloudformation validate-template \
		--template-body file://stacks/s3-basic-auth.yaml
