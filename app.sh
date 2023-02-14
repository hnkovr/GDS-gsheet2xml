echo Starting app.sh...

alias pip=pip3
alias python=python3

pip install virtualenv
virtualenv .env_name_1
source .env_name_1/bin/activate

pip install -r requirements.txt
pip install uvicorn

uvicorn main:app --reload

echo app.sh has been started!