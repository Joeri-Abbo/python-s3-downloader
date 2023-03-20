import boto3

if __name__ == '__main__':
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    with open("downloader.sh", "w") as file:

        for bucket in response['Buckets']:
            file.write(f'aws s3 sync s3://{bucket["Name"]} {bucket["Name"]}\n')
            file.write('')
