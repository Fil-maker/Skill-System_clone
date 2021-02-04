# skill-management-system

## How to run
* Clone this [repository](https://github.com/sssemion/skill-management-system)

* Create virtual environment with python 3.7.x and not any other

* Install requirements with `pip install -r requirements.txt`

* Create `.env` file in root directory with that code
```dotenv
API_PORT="5000"
API_HOST="127.0.0.1"
API_DEBUG=0

APP_PORT="8080"
APP_HOST="127.0.0.1"
APP_DEBUG=0

CHECK_PASSWORD_STRENGTH=1
SKILL_NAME="<Skill name>"

# Postresql connection
PG_USER="YOUR_DB_LOGIN"
PG_PASS="YOUR_DB_PASSWORD"
PG_HOST="YOUR_DB_HOST"
DB_NAME="YOUR_DB_NAME"

# SMTP connetcion
MAIL_SERVER="smtp.googlemail.com"
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME="YOUR_MAIL_BOX"
MAIL_PASSWORD="YOUR_MAIL_BOX_PASSWORD"

# S3 bucket connection
S3_BUCKET_NAME="YOUR_S3_BUCKET_NAME"
S3_BUCKET_URL="YOUR_S3_BUCKET"

# Security tokens, secret keys etc.
API_SECRET="SECRET"
APP_SECRET="SECRET"
```

### Configuring the database
1. Set the project path as the `PYTHONPATH` environment variable. Example:
   ```
    Windows:
   set PYTHONPATH=C:\Users\<username>\PycharmProjects\skill-management-system
   
   # Linux:
   export PYTHONPATH=~/skill-management-system
   ```
   
2. Initialize the database with this command:
    ```commandline
    python3 api/data/manage.py initialize_db
    ```

### Configuring access to AWS S3 Bucket
1. Make your S3 Bucket public to read. To do that:
    + Turn off blocking of public access
    + Set the following bucket policy, replacing `<YOUR_S3_BUCKET_NAME>` with the name of your bucket:
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowPublicRead",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::<YOUR_S3_BUCKET_NAME>/*"
            }
        ]
    }
    ```

1. Create new IAM User [here](https://console.aws.amazon.com/iam/home#/users$new?step=details):
    + Set user name and access type - Programmatic access
    + Choose "Attach existing policies directly", click "Create policy":
        - Switch to "JSON"
        - Paste the following, replacing `<YOUR_S3_BUCKET_NAME>` with the name of your bucket:
        ```json
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:PutObject",
                        "s3:DeleteObject"
                    ],
                    "Resource": "arn:aws:s3:::<YOUR_S3_BUCKET_NAME>/*"
                }
            ]
        }
        ```
        - Click "Review policy", set policy name and confirm creation
        - On the previous page select the policy you have just created
    + Add tags (optional)
    + Review and confirm creating
    + Save `Access key ID` and `Secret access key` or download `.csv`

2. Create file `~/.aws/config` with the following text
    ```
    [default]
    region = YOUR_AWS_REGION
    ``` 

3. Create file `~/.aws/credentials` replacing `ACCESS_KEY_ID` and `SECRET_ACCESS_KEY` with keys you saved on step 1
    ```
    [default]
    aws_access_key_id = ACCESS_KEY_ID
    aws_secret_access_key = SECRET_ACCESS_KEY
    ```
   > WARNING! Do not use keys with root access to the cloud!

* Run `api_runner.py`

* Run `app_runner.py`
