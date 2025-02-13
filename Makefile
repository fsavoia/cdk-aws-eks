.PHONY: test

# Define the default target
test: 
	@AWS_DEFAULT_REGION=us-east-1 pytest -vv

# Clean up pytest cache and temporary files
clean:
	@rm -rf .pytest_cache
	@rm -rf __pycache__

# Install dependencies
install:
	@. .venv/bin/activate
	@pip install -r requirements-dev.txt
	@pip install -r requirements.txt

# Install dev dependencies
dev-install:
	@pip install -r requirements-dev.txt

# Bootstrap the AWS environment for CDK
bootstrap:
	@JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=true cdk bootstrap

# Deploy the CDK stack
deploy:
	@JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=true cdk deploy --all --no-rollback --require-approval never

# Destroy the CDK stack
destroy:
	@JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=true cdk destroy --all -f

# Check env drift the CDK stack
diff:
	@JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=true cdk diff

# Check env drift the CDK stack
synth:
	@JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=true cdk synth
