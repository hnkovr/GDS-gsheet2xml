#!/bin/bash

if [[ "$*" == *"--debug"* ]]; then
  echo "Running with DEBUG mode (echo all executing bash,..?)"
  set -x  # enable debug mode
else
  echo "Use --debug for running with DEBUG mode"
fi

echo "The first argument is: $1"
echo "The second argument is: $2"
echo "The second argument is: $3"

PYTHON="python-3.9.16"

# Heroku app name
APP_NAME="gsheet-to-xml$1"  #! Find&Replace all
echo Starting app $APP_NAME

##? 1st login
#todo: add?
#heroku auth
#heroku login

# create a new Heroku app

#todo: add:
#heroku drop $APP_NAME  #:  ›   Warning: drop is not a heroku command.
                           #Did you mean stop? [y/n]:
                           # ›   Error: Run heroku help for a list of available commands.

heroku create $APP_NAME

# set the Python buildpack
heroku buildpacks:set heroku/python

#fixme:
#`Creating heroku-postgresql:hobby-dev on ⬢ gsheet-to-xml7... !
   # ▸    Couldn't find either the add-on service or the add-on plan of
   # ▸    "heroku-postgresql:hobby-dev".
## add postgres add-on to the app
#heroku addons:create heroku-postgresql:hobby-dev
##`? get the URL of the Postgres database
#DATABASE_URL=$(heroku config:get DATABASE_URL)


# create a `Procfile` in the root of your project with the following contents:
# web: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT --workers 1" > Procfile

# create a new file `runtime.txt` in the root of your project with the following contents:
echo # echo "python-3.11.2" > runtime.txt
echo $PYTHON > runtime.txt

## create a new file `requirements.txt` in the root of your project with the following contents:
# Using exising after dedup lines!
#python util --dedup_lines requirements.txt
#echo "fastapi" >> requirements.txt
#echo "uvicorn" >> requirements.txt
#echo "sqlalchemy" >> requirements.txt
#echo "# app <$APP_NAME> was used!" >> requirements.txt

echo # add all files to Git and push to Heroku
git init
git add .

#todo: add
#!wr git diff --cached

git commit -m "Initial commit"
heroku git:remote -a $APP_NAME
git push heroku master
git push heroku main

# Check if --run argument is present
if [[ "$*" == *"--run"* ]]; then
  echo "Running the deployed solution:.."
  # do something when --run is present
  sh heroku_2_run.sh
else
  echo "Not running the deployed solution."
  # do something when --run is not present
fi

echo # View logf
heroku logs --tail

set +x  # disable debug mode
