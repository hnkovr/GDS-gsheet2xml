from fastapi import FastAPI, Response

from SpreadsheetToXML import gsheet2xml
from util import ef, output_by_all_logging_ways

app = FastAPI()


@app.get("/gsheet2xml/{gsheet_id}")
def process(gsheet_id: str):
    res_xml = gsheet2xml(gsheet_id=gsheet_id)
    ## `return res_xml
    return {"gsheet_id": gsheet_id, "res_xml": res_xml}


@app.get("/xml/{gsheet_id}")
@ef
def xml_endpoint(gsheet_id: str):
    # xml_str = "<data><item>1</item><item>2</item><item>3</item></data>"
    xml_str = gsheet2xml(gsheet_id=gsheet_id)
    response = Response(content=xml_str, media_type="application/xml")
    return response


@app.get("/")
def read_root(): return {"Hello": "World"}


def main():
    files = "app.py app.sh".split(' ')
    output_by_all_logging_ways(
        f"For check run on of {files} and click this: http://127.0.0.1:8000/gsheet2xml/1x9sIJcJ857u2V7GV9gdlgjzng6jyPpK9Hh4O-GOi8PE"
    )


if __name__ == '__main__': main()
