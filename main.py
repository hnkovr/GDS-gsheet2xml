from fastapi import FastAPI
from util import log, ef
from SpreadsheetToXML import gsheet2xml

app = FastAPI()


@app.get("/gsheet2xml/{gsheet_id}")
@ef
def process(gsheet_id: str):
    res_xml = gsheet2xml(gsheet_id=gsheet_id)
    ## `return res_xml
    return {"gsheet_id": gsheet_id, "res_xml": res_xml}


@app.get("/")
def read_root(): return {"Hello": "World"}

if __name__ == '__main__':
    print(
        f"For check click this: http://127.0.0.1:8000/gsheet2xml/1x9sIJcJ857u2V7GV9gdlgjzng6jyPpK9Hh4O-GOi8PE"
    )
# from heroku_0_init import final_state
# > ImportError: cannot import name 'final_state' from 'heroku_0_init' (/Users/user/github/hnkovr/gsheet2xml/./heroku_0_init.py)
