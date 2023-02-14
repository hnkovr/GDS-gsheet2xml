#!/bin/bash

# Heroku app name
APP_NAME="gsheet-to-xml"

# create a new Heroku app
heroku create $APP_NAME

# set the Python buildpack
heroku buildpacks:set heroku/python

# add postgres add-on to the app
heroku addons:create heroku-postgresql:hobby-dev

# get the URL of the Postgres database
DATABASE_URL=$(heroku config:get DATABASE_URL)

# create a `Procfile` in the root of your project with the following contents:
# web: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT --workers 1" > Procfile

# create a new file `runtime.txt` in the root of your project with the following contents:
# python-3.9.9
echo "python-3.9.9" > runtime.txt

# create a new file `requirements.txt` in the root of your project with the following contents:
# fastapi
# uvicorn
# sqlalchemy
echo "fastapi" > requirements.txt
echo "uvicorn" >> requirements.txt
echo "sqlalchemy" >> requirements.txt

# add all files to Git and push to Heroku
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a $APP_NAME
git push heroku master
