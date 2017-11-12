Enforce HTTP Basic Authentication for S3 buckets with CloudFront and Lambda@Edge.

## How It Works?
The implementation relies on AWS CloudFront and Lambda@Edge functions to implement
basic authentication for Amazon S3 bucket. CloudFront is used as a frontend to
S3 access. A custom lambda function intercepts all requests to the CloudFront
distribution and checks them for valid basic auth credentials as follows:

* If the request doesn't have an `Authorization` header, it returns a 401
  Unauthorized response to the client with a `WWW-Authenticate: Basic`
  header to trigger Basic Auth prompt the client browser.
* If the request contains an `Authorization` header, the token is compared
  against pre-configured credentials. If the credentials match, the request
  is approved. If the credentials are invalid, a 403 Forbidden response is
  sent to the client.

The setup also includes a custom CloudFront Origin Access Identity that is used
to access the origin bucket in S3. It creates a bucket policy for the target
bucket that allows access from this custom OAI only. That is, the bucket cannot
be accessed directly but all requests must go through the CloudFront distribution.

## Deployment
The deployment of this setup is fully automated via CloudFormation. The `stacks/`
directory contains a CloudFormation template ([s3-basic-auth.yaml](stacks/s3-basic-auth.yaml))
that sets everything up. It takes the following parameters:

* `AuthorizationCredentials` - base64 encoded credentials that grant access to the bucket
* `OriginBucketName` - the name of the S3 bucket to provide protected access to
* `UpdateTime` - current timestamp (value is not important; should be different from
  previous oneex)

`AuthorizationCredentials` can be generated as follows (replace `username` and `password`
with the respective values):
```
echo -n "username:password" | base64
```

### Deploying the Stack
To deploy the stack, run the following:
```
make create-basic-auth AUTHORIZATION_CREDENTIALS=<base64 credentials> ORIGIN_BUCKET_NAME=<your bucket>
```

To update the stack, run the following:
```
make update-basic-auth AUTHORIZATION_CREDENTIALS=<base64 credentials> ORIGIN_BUCKET_NAME=<your bucket>
```

You can also deploy the stack directly with the AWS CLI or Console.
