# Install, Deploy and Run from terminal
```bash
echo # https://chat.openai.com/chat/25635f5c-425a-4c4b-b0ca-114fe27dcc8d
export PROJECT_NUMBER=8
export $TMP_PATH=tmp123
set -x  # enable debug mode

echo # https://www.google.com/search?client=firefox-b-d&q=how+in+bash+to+check+and+remove+some+set+by+variable+dir+if+it+exists%2C+then+make+new+one+with+the+same+name+and+finally+chage+path+to+this+dir+path%3F
rm -r $TMP_PATH
mkdir $TMP_PATH
cd $TMP_PATH
gh repo clone hnkovr/GDS-gsheet2xml
cd GDS-gsheet2xml
sh heroku_1_deploy.sh $PROJECT_NUMBER --debug
sh heroku_2_run.sh
```

## 1 Install from repo & console
```shell
gh repo clone hnkovr/GDS-gsheet2xml
sh heroku_1_deploy.sh
```

## 2 Deploy & run (optinal) from IDE
```shell
sh heroku_1_deploy.sh
```

More examples of using:
```shell
# deploy to app #5 & run after
sh heroku_1_deploy.sh 5 --run
```

Deploy to set project number (number'll be in the end of the domain of the project url, e.g. for PROJECT_NUMBER=7 link'll of started service be: xxx
‼️ Be aware, when you deploy project with some number, previous version of the same numbered project'll be overwritten!
```shell
sh heroku_1_deploy.sh <PROJECT_NUMBER> --debug
```

## 3 Only run
```shell
sh heroku_2_run.sh
```

## 4 Drop app by number:
```bash
sh heroku_3_drop_app_by_nr.sh <PROJECT_NUMBER>
```

## 5 Local development & debug:
For this purposes use app.py or app.sh

* original github link: https://github.com/hnkovr/GDS-gsheet2xml 
* link for local testing check:  
* link for test on web: /xml/1x9sIJcJ857u2V7GV9gdlgjzng6jyPpK9Hh4O-GOi8PE
* last demo link: https://gsheet-to-xml5.herokuapp.com/xml/1x9sIJcJ857u2V7GV9gdlgjzng6jyPpK9Hh4O-GOi8PE