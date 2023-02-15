#!/bin/bash

## Heroku app name
APP_NAME="gsheet-to-xml7"

# start the app
heroku ps:scale web=1 --app $APP_NAME

heroku logs --tail