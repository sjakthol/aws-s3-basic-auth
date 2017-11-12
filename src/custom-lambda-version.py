#!/usr/bin/env python3
import boto3
import cfnresponse

client = boto3.client('lambda')

def handler(event, context):
    print('Received request', event)
    properties = event['ResourceProperties']
    phyid = event.get('PhysicalResourceId', '%s/%s' % (event['StackId'], event['LogicalResourceId']))
    if 'FunctionName' not in properties:
        print('ERROR: FunctionName missing')
        return cfnresponse.send(event, context, cfnresponse.FAILED, {}, phyid)

    if event['RequestType'] in ('Create', 'Update'):
        latest = None
        latest_version = 0
        latest_published = None
        while True:
            res = client.list_versions_by_function(FunctionName=properties['FunctionName'])

            for version in res['Versions']:
                if version['Version'] == '$LATEST':
                    latest = version
                elif int(version['Version']) > latest_version:
                    latest_version = int(version['Version'])
                    latest_published = version

            if 'NextMarker' not in res:
                print('DEBUG: Found all versions')
                break

        if latest_published and latest['CodeSha256'] == latest_published['CodeSha256']:
            # No code changes. Don't publish
            print('DEBUG: No changes since last update')
            return cfnresponse.send(event, context, cfnresponse.SUCCESS, {
                'LatestVersion': latest_published['Version'],
                'LatestVersionArn': latest_published['FunctionArn']
            }, phyid)

        # Some changes made. Publish a new version
        res = client.publish_version(FunctionName=properties['FunctionName'])

        return cfnresponse.send(event, context, cfnresponse.SUCCESS, {
            'LatestVersion': res['Version'],
            'LatestVersionArn': res['FunctionArn']
        }, phyid)

    elif event['RequestType'] == 'Delete':
        return cfnresponse.send(event, context, cfnresponse.SUCCESS, {}, phyid)

if __name__ == '__main__':
    class ctx:
        log_stream_name = 'log_stream_name'
    handler({
        'RequestType': 'Update',
        'RequestId': 'request-1',
        'StackId': 'stack-2',
        'LogicalResourceId': 'resource-1',
        'ResponseURL': 'http://localhost:8080',
        'PhysicalResourceId': 'stack-2/resource-1',
        'ResourceProperties': {
            'FunctionName': 'ue1-s3-basic-auth-AuthenticatorLambda-OG6ZWEUR8BMC'
        }
    }, ctx)
