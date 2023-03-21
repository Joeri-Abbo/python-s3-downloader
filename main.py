import boto3
import os

if __name__ == '__main__':
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    path = os.path.abspath(os.getcwd())

    with open("downloader.sh", "w") as file:
        for bucket in response['Buckets']:
            file.write('')
            file.write(f'echo "{bucket["Name"]}"\n')
            file.write(f"if [ -e {bucket['Name']}.tar.gz ]\n")
            file.write(f"then\n")
            file.write(f"tar -xvf {bucket['Name']}.tar.gz\n")
            file.write(f"fi\n")
            file.write(f'aws s3 sync s3://{bucket["Name"]} {bucket["Name"]}\n')
            file.write(f"tar -czvf {bucket['Name']}.tar.gz {bucket['Name']}\n")
            file.write(f"rm -rf {bucket['Name']}\n")
            file.write('')
