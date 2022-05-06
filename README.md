# DJ Spoofer - Django + Web Scraping Made Easy

[![codecov](https://codecov.io/gh/adrianmeraz/dj-spoofer/branch/master/graph/badge.svg?token=SV085I4DGJ)](https://codecov.io/gh/adrianmeraz/dj-spoofer)
![test-status](https://github.com/adrianmeraz/dj-spoofer/actions/workflows/dev.yml/badge.svg?branch=dev)

## Setup Local Dev Environment

### Setup SSH Keys

#### Generate SSH Keys

Run command:

`ssh-keygen -t rsa -b 4096 -C "your_email@domain.com"`

Hit enter to accept default file location, and again to accept empty passphrase

#### Copy Public Key

Install xclip

`sudo apt-get install xclip`

To copy to clipboard, run:

`xclip -sel clip < ~/.ssh/id_rsa.pub`

### Install git

```
sudo apt install git-all
```

### Install IntelliJ Toolbox

Download tarball from [HERE](https://www.jetbrains.com/toolbox-app/)

Extract tarball and replace `<VERSION>` with the actual package name:

`sudo tar -xzf jetbrains-toolbox-<VERSION>.tar.gz -C /opt`

Run the install script. Replace `<VERSION>` with the actual package name:

```
cd /opt/jetbrains-toolbox-<VERSION>
./jetbrains-toolbox
```

Follow prompts and install Pycharm Community IDE

### Install Curl

`sudo snap install curl`

### Install python-venv

`sudo apt install python3.9-venv`

### Install distutils

`sudo apt install python3-distutils`

### Install Poetry

```
sudo curl -sSL https://install.python-poetry.org | python3 -
```

### Add Poetry Env Variable

Append the following to `~/.profile`

`export PATH="/home/adrian/.local/bin:$PATH`

Test the poetry install:

`poetry --version`

### Pull Dev Repo

Create project directory and initialize Git

`git init`

Add Remote Origin

`git remote add origin git@github.com:adrianmeraz/marz-explorer.git`

Pull repo

`git pull`

Create new branch and switch to branch

`git checkout -b <BRANCH_NAME>`

Delete local branch

`git branch -d <BRANCH_NAME>`

### Add .env file

Use .env example to set environment variables.

**NOTE**

When deploying to remote environments, the environment variables must be set in Git secrets, as well as
the lambda deployment.

### Verify Github Action Secret

`DATABASE_URL` should be set to `postgres://postgres:postgres@localhost:5432/postgres`

This should match values in the github actions yml

### Install Poetry

Install poetry with instructions [HERE](https://python-poetry.org/docs/#installation)

Verify the installation with a version check

`poetry --version`

If command not found, set the path variable:

`source $HOME/.poetry/env`

### Install Dependencies

`poetry install`

### Generate the secret key
```
import secrets

print(secrets.token_urlsafe())
```

Add to .env file as _SECRET_KEY_ environment variable

## Local Database Setup

### Setup Postgres Local Instance (Ubuntu)

```
sudo apt update
sudo apt install postgresql postgresql-client
```

### Check Instance Status

```
systemctl status postgresql.service
```

### Change System User Password

**NOTE: Don't use the @ symbol in the password!**

```
sudo su - postgres
psql -c "alter user postgres with password '<DB_PASSWORD>'"
```

### Start PSQL Shell

`psql`

### Get Connection Details

`\conninfo`

Details should look similar to this:
```
You are connected to database "postgres" as user "postgres" via socket in "/var/run/postgresql" at port "5432".
```

### Create Local Postgres Database

Log into postgres database

```
sudo -u postgres psql
```

The postgres shell is started and the prompt should start with `postgres=#`

Replace placeholder values with real values

```
create database <DB_NAME>;
create user <DB_USERNAME> with encrypted password '<DB_PASSWORD>';
postgres=# grant all privileges on database <DB_NAME> to <DB_USERNAME>;
postgres=# ALTER USER <DB_USERNAME> CREATEDB;
```

### Local jdbc string

`postgres://<DB_USERNAME>:<DB_PASSWORD>@localhost:5432/<DB_NAME>`

### Deleting Local Database (Optional)

Start the Postgres Shell:

```
sudo -u postgres psql
```

Run:

```
DROP DATABASE <DB_NAME>;
```


### Create Database on Existing Instance using admin command (Optional)

The initial database url <DB_INSTANCE_URL> will be:

`postgres://postgres:<PASSWORD>@localhost:5432/postgres`

Run the command from the project root to create the database and service user

`poetry run python manage.py create_db --db-url="<DB_INSTANCE_URL>" --db-name="<NEW_DB_NAME>" --db-username="<NEW_DB_USERNAME>" --db-password="<NEW_DB_PASSWORD>"`

## PGAdmin

### Installation

#### Install the public key

Install the public key for the repository (if not done previously):

```
sudo curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add
```

#### Create the repository configuration file:

```
sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/focal/ pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
```

####  Install for both desktop and web modes:

```
sudo apt install pgadmin4
```

### Initialize Database

```
poetry run python manage.py makemigrations
poetry run python manage.py migrate
git add .
poetry run python manage.py createsuperuser
```

### Create Super User

Set the following environment variables:

DJANGO_SUPERUSER_EMAIL
DJANGO_SUPERUSER_USERNAME
DJANGO_SUPERUSER_PASSWORD

```
poetry run python manage.py makemigrations
poetry run zappa manage <STAGE_NAME> "migrate"
poetry run zappa manage <STAGE_NAME> "createsuperuser --noinput"
```

## Admin Commands

### Add Rotating Proxy

```
djspoofer_add_rotating_proxy --proxy-url "premium.residential.proxyrack.net:10000" --settings=config.settings.local
```

### Create desktop fingerprints

```
djspoofer_create_desktop_fingerprints --num_to_create "10" --settings=config.settings.local
```

### Get all Intoli Profiles

```
intoli_get_profiles --settings=config.settings.local
```

### Save H2 Hash

```
save_h2_hash --hash "1:65536;2:1;3:1000;4:6291456;5:16384;6:262144|15663105|1:1:0:256|m,a,s,p" --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36" --browser-min-major-version 60 --browser-max-major-version 110 --settings=config.settings.local
```

### Get all Chrome fingerprints report

```
djspoofer_all_chrome_fingerprints --proxy-url "premium.residential.proxyrack.net:10000" --proxy-args "country=US" --settings=config.settings.local
```

## Poetry Utilities

### Create Initial Poetry File
```
poetry init
```

### Install All Requirements
```
poetry install
```

### Update all Poetry Packages
```
poetry update
```

### Update Individual Poetry Package
`poetry update <PACKAGE_NAME>`

### View All Requirements
`poetry show --tree`

### List Virtual Envs
`poetry env list`

### Get Poetry Env Info
`poetry env info`

### Remove Virtual Env
`poetry env remove <ENV_NAME>`

### Clear Cache
`poetry cache clear . --all`

### Poetry Executable Path
`which poetry`

## Database Utilities

### Migrations

After any Model Updates:
1. Create migrations
2. Add migrations to git
3. Migrate to run DB changes

```
poetry run python manage.py makemigrations
poetry run python manage.py migrate
git add .
poetry run python manage.py createsuperuser

```

## Proxy Backends

### ProxyRack Backend

To set custom weights when selecting countries for geolocation, 
use the PROXYRACK_COUNTRY_WEIGHTS setting.

Example:

```
PROXY_COUNTRY_WEIGHTS = [
    ('US', .70),
    ('CA', .12),
    ('UK', .12),
    ('AU', .06),
]
```

PROXYRACK_COUNTRY_WEIGHTS

## Testing

Specify settings with `--settings`

### Running tests

`poetry run python manage.py test --settings=config.settings.local --no-input --parallel`

To run against a single module, add the module name:

`poetry run python manage.py test djspoofer.tests.test_views --settings=config.settings.local --no-input`

### Faster Tests

**NOTE** Tests must be isolated and able to run independently! The `--parallel` flag causes incorrect values

```
coverage run manage.py test --settings=config.settings.local --keepdb
```

### Generate Coverage Report

Must be run after coverage tests have been run

```
coverage report
```

### Generate Coverage HTML Report

```
coverage html
```

This creates the directory coverage html. Open the index.html to see the full report

### Coverage Issues

If the numbers reported aren't what's expected, or tests are missing, verify that an empty `__init__.py`
is in the `tests` directory for each app.

---

## Contributions

Contributions are encouraged and welcome! 

The general steps to contribute are:

1. Create an issue for a feature/bug, if not already created
2. Create a feature branch with the issue in the name
   1. Example: If the issue is `#123`, create the branch as `feature/DC-123`
3. Write Tests
4. Write Code - All code must have tests and cannot lower coverage!
5. Verify all tests pass
6. Pull all and merge all changes from the dev branch
7. Create a pull request to merge into the dev branch