# https://chat.openai.com/chat/9553edcf-08ba-4e36-8eaf-52aa393e7733
import xml.etree.ElementTree as ET
from textwrap import shorten

import gspread
import numpy as np
import pandas as pd
from fastcore.all import *
from fastcore.all import basic_repr
from oauth2client.service_account import ServiceAccountCredentials

from config import CONFIG
from gdown import gdown
from util import log, ef, logd


class SpreadsheetToXML:
    __repr__ = basic_repr
    logd(f"{ CONFIG = }")
    creds_file: str
    output_file: str
    use_creds_file: bool  # use existing file
    creds_gdrive_id: str
    return_fpath: bool
    gsheet_id: str

    @ef
    def __init__(self, gsheet_id: str, *,
                 creds_file: str = CONFIG.creds_file,
                 use_creds_file: bool = CONFIG.use_creds_file,
                 creds_gdrive_id: str = CONFIG.creds_gdrive_id,
                 return_fpath: bool = CONFIG.return_fpath,
                 output_file: str = CONFIG.output_file,
                 warn=log.warning,
                 scope=CONFIG.SCOPE,
                 ):

        store_attr()

        self.creds_file_content = os.getenv(creds_file, None)
        if self.creds_file_content:
            warn(f"! Using existing in <os.getenv('{creds_file=}')> creds: {shorten(os.getenv(creds_file), 333)}")
        elif creds_file and use_creds_file:
            creds_gdrive_id = None
            warn(f"! Using existing creds: use_creds_file={use_creds_file}: exising <{creds_file}>'ll be used!")

        xxx = (self.creds_gdrive_id, self.creds_file, self.creds_file_content)
        assert any(xxx) and not all(xxx), f"Should be any, but not all of {xxx = }"

        # self.scope = CONFIG.SCOPE
        # assert all((self.scope,))
        # store_attr()

    @ef
    def run(self, return_fpath: bool = None):
        return_fpath = return_fpath or self.return_fpath
        need_gdown = False
        if self.creds_file_content:
            self.creds_file = f"{self.creds_file}.tmp"
            with open(self.creds_file, 'w') as f:
                f.write(self.creds_file_content)
        elif not self.creds_file:
            need_gdown = True
        elif not os.path.isfile(self.creds_file):
            need_gdown = True
        if need_gdown:
            assert self.creds_gdrive_id, f"! For downloading {self.creds_gdrive_id = } should be not empty!"
            self.creds_file = gdown(f'https://drive.google.com/uc?id={self.creds_gdrive_id}')
            logd(f"! Using downloaded creds: {self.creds_file = }")

        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.creds_file, self.scope)
        gc = gspread.authorize(credentials)
        sh = gc.open_by_key(self.gsheet_id)
        worksheet = sh.sheet1

        df = pd.DataFrame(worksheet.get_all_records())
        df.replace("", np.nan, inplace=True)
        df.fillna(method='ffill', inplace=True)

        root = ET.Element("conversations")
        grouped = df.groupby(["Conversation ID", "Prompt"])
        for (conversation_id, prompt), group in grouped:
            conversation = ET.SubElement(root, "conversation", id=str(conversation_id))
            prompt_element = ET.SubElement(conversation, "prompt")
            prompt_element.text = prompt
            response_options = ET.SubElement(conversation, "response_options")
            classification_grouped = group.groupby("Classification")
            for classification, classification_group in classification_grouped:
                response = ET.SubElement(response_options, "response", classification=classification)
                feedback = classification_group["Feedback"].iloc[0]
                next_conversation_id = classification_group["Next Conversation ID"].iloc[0] if not pd.isna(
                    classification_group["Next Conversation ID"].iloc[0]) else None
                for index, row in classification_group.iterrows():
                    text = ET.SubElement(response, "text")
                    text.text = row["Text"]
                feedback_element = ET.SubElement(response, "feedback")
                feedback_element.text = feedback
                if next_conversation_id is not None:
                    next_conversation_id_element = ET.SubElement(response, "next_conversation_id")
                    next_conversation_id_element.text = str(next_conversation_id)

        logd("# Write the XML file:..")
        tree = ET.ElementTree(root)
        tree.write(self.output_file, encoding="utf-8", xml_declaration=True)
        logd(f"# Write the XML file: {self.output_file=}")

        if return_fpath:
            return os.path.join(os.getcwd(), self.output_file)
        else:
            with open(self.output_file, 'r') as f:
                return f.read()
            # return tree


@ef
def gsheet2xml(gsheet_id: str, **kwargs):
    return SpreadsheetToXML(gsheet_id=gsheet_id, **kwargs).run()


def test1():
    print(f"> {gsheet2xml(gsheet_id = '1x9sIJcJ857u2V7GV9gdlgjzng6jyPpK9Hh4O-GOi8PE') = }")


if __name__ == '__main__': test1()
