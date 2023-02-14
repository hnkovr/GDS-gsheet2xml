#!/bin/bash

# Heroku app name
APP_NAME="xxxgsheet-to-xml"

# start the app
heroku ps:scale web=1 --app $APP_NAME
