# skill-management-system

## How to run
* Clone this [repository](https://github.com/sssemion/skill-management-system)
* Create virtual environment with python 3.7.x and not any other
* Install requirements with `pip install -r requirements.txt`
* Create `api_runner.py` in root directory with that code
```
import os
import api


def run():
    api.app.run(host=os.environ.get("API_HOST"),
                port=os.environ.get("API_PORT"),
                debug=int(os.environ.get("API_DEBUG")))


if __name__ == '__main__':
    run()
``` 

* Create `runner.py` in root directory with that code
```
import os
import app


def run():
    app.app.run(host=os.environ.get("APP_HOST"),
                port=os.environ.get("APP_PORT"),
                debug=int(os.environ.get("APP_DEBUG")))


if __name__ == '__main__':
    run()
``` 

* Create `.env` file in root directory with that code
```
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

* Create file `config` in `C:\Users\<username>\.aws` with that text inside
```
[default]
region = YOUR_AWS_REGION
``` 

* Create file `credentials` in the same directory with that text inside
```
[default]
aws_access_key_id = YOUR_AWS_ACCESS_KEY
aws_secret_access_key = YOUR_AWS_SECRET_KEY
```

* Run `api_runner.py`

* Run `app_runner.py`