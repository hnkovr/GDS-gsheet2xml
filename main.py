from SpreadsheetToXML import gsheet2xml

from fastapi import FastAPI

app = FastAPI()


@app.get("/gsheet2xml/{gsheet_id}")
def process(gsheet_id: str):
    res_xml = gsheet2xml(gsheet_id=gsheet_id)
    ## `return res_xml
    return {"gsheet_id": gsheet_id, "res_xml": res_xml}


@app.get("/")
def read_root(): return {"Hello": "World"}
