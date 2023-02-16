#!/bin/bash
source heroku_0_config.sh

## Heroku app name
APP_NAME="$APP_NAME"

# start the app
heroku ps:scale web=1 --app $APP_NAME

heroku logs --tail