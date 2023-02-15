#!/bin/bash
PYTHON="python-3.9.16"

# Heroku app name
APP_NAME="gsheet-to-xml7"  #! Find&Replace all
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
#echo "python-3.11.2" > runtime.txt
echo $PYTHON > runtime.txt

## create a new file `requirements.txt` in the root of your project with the following contents:
# Using exising after dedup lines!
#python util --dedup_lines requirements.txt
#echo "fastapi" >> requirements.txt
#echo "uvicorn" >> requirements.txt
#echo "sqlalchemy" >> requirements.txt
echo "# app <$APP_NAME> was used!" >> requirements.txt

# add all files to Git and push to Heroku
git init
git add .

#todo: add
#!wr git diff --cached

git commit -m "Initial commit"
heroku git:remote -a $APP_NAME
git push heroku master
git push heroku main

# View logf
heroku logs --tail

#todo: if $RUN_AFTER_DEPLOY
sh heroku_2_run.sh
heroku logs --tail
