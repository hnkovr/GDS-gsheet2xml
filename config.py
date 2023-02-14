from typing import List

from fastcore.all import basic_repr

from util import load_key


class CONFIG:
    YAML = 'config.yaml'
    creds_file: str = 'creds.json'
    output_file: str = 'output.xml'
    use_creds_file: bool = False  # use existing file
    creds_gdrive_id: str = load_key(YAML, 'creds_gdrive_id')
    SCOPE: List[str] = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    return_fpath: bool = False
    __repr__ = lambda: basic_repr('return_fpath,creds_file,use_creds_file,output_file,scope')


def test():
    print(
        f"# {CONFIG = }",
        f"# {CONFIG.creds_gdrive_id = }",
        sep='\n'
    )


if __name__ == '__main__': test()
