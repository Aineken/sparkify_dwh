import configparser
import boto3

# Load AWS credentials from the config file
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))
KEY = config.get('AWS', 'key')
SECRET = config.get('AWS', 'secret')

# Initialize the S3 client
s3_client = boto3.client('s3',
                         region_name="us-west-2",
                         aws_access_key_id=KEY,
                         aws_secret_access_key=SECRET
                        )

# Download log_json_path.json
s3_client.download_file('udacity-dend', 'log_json_path.json', 'samples/log_json_path.json')

# Download 2018-11-12-events.json
s3_client.download_file('udacity-dend', 'log_data/2018/11/2018-11-12-events.json', 'samples/2018-11-12-events.json')

# Download the sample of song dataset
s3_client.download_file('udacity-dend', 'song_data/A/B/C/TRABCEI128F424C983.json', 'samples/TRABCEI128F424C983.json')


print("Files downloaded successfully!")
