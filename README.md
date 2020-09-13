# Flask JWT auth system with Flask Admin Page

## Intro 
Written in flask using Python3.
It uses postgres as database.
It is currently, deployed on Heroku.

Basically swagger docs can be accessed at `https://flask-admin-jwt.herokuapp.com/`

it has two namespace apis, one `auth` for login, logout, etc

another for listing users info accessed by admin only `/user/`

admin token is need to access force-logout and expire token or list user endpoints

on logout token is blacklisted and jti stored in db

## To Run in Local 
## requires postgres running locally
`virtaulenv -p python3 venv` - to setup virtualenv

`source venv/bin/activate` - to activate env

`source env_vars/dev.sh` - to set up env vars. create a dev.sh file using template in env_vars/dummy.sh

`python manage.py db init` - to init migrations  `flask db init` can also be used

`python manage.py db migrate` - to migrate  `flask db migrate` can also be used

`python manage.py db upgrade` - to apply latest migrations  `flask db upgrade` can also be used

`python wsgi.py` - to run app
