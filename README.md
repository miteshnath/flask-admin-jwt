# Flask JWT auth system with Flask Admin Page

## Intro 
Written in flask using Python3.
It uses postgres as database.
Also uses redis for storing active JTI 
It is currently, deployed on Heroku at  

## To Run in Local 
## requires postgres running locally
`virtaulenv -p python3 venv` - to setup virtualenv
`source venv/bin/activate` - to activate env
`source env_vars/dev.sh` - to set up env vars. create a dev.sh file using template in env_vars/dummy.sh
`python manage.py db init` - to init migrations  `flask db init` can also be used
`python manage.py db migrate` - to migrate  `flask db migrate` can also be used
`python manage.py db upgrade` - to apply latest migrations  `flask db upgrade` can also be used
`python wsgi.py` - to run app
