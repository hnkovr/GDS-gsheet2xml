import os
import sys
from textwrap import shorten
from typing import Optional, Any, Callable

import yaml
from loguru import logger as log


class FileNotFoundError(Exception): pass


def is_good_fyaml(filename):
    try:
        return bool(yaml.full_load(filename))
    except:
        log.exception()
        return False


def save_key(filename: str, key: str, value: Any) -> Optional[str]:
    if os.path.exists(filename): assert is_good_fyaml(filename)
    with open(filename, 'w') as f: yaml.dump({key: value}, f)
    return os.path.join(os.getcwd(), filename)


def load_key(filename: str, key: str, *, skip_err: bool = True, loader: Callable = yaml.unsafe_load) -> Optional[str]:
    if not os.path.exists(filename):
        if not skip_err:
            raise FileNotFoundError(filename)
        else:
            return
    with open(filename, 'r') as f:
        data = loader(f)
        assert data, f"Data's not been loaded from <{filename}>!"
        return data.get(key)


def fprint(yaml_fname, max_len=1111, print=print):
    with open(yaml_fname) as f: print(f"File <{yaml_fname}> content:\n{shorten(f.read(), max_len)}\n{'*' * 88}")


class Tests:
    DEBUG = False
    YAML_FNAME = 'test.yaml'

    @classmethod
    def test1(cls):
        print(
            f"{is_good_fyaml(cls.YAML_FNAME) = }"
        )

    @log.catch
    @staticmethod
    def test(cls):
        YAML_FNAME = cls.YAML_FNAME
        KEY_NAME, VALUE = 'API_KEY', 'test123'
        try:
            save_key(YAML_FNAME, KEY_NAME, VALUE)
            fprint(YAML_FNAME)
            print(f"# {load_key(YAML_FNAME, KEY_NAME) = }")
        finally:
            if not cls.DEBUG:
                os.remove(YAML_FNAME) if os.path.isfile(YAML_FNAME) else print(f"File <{YAML_FNAME}>'s not exist.")


# from bash import bash
# def bash(*cmd, bash=bash):
#     cmd = ' '.join(cmd)
#     print(f"$ {cmd}")
#     res = bash(cmd)
#     print(f"> {res}")

@log.catch
def init_loguru():
    format = None
    # format = '{time:YY/MM/DD HH:mm:ss} {level.name[0]} "{file.path}", line {line}: {message}'

    log.remove()  # remove any existing handlers
    kwargs = dict(format=format,
                  level="DEBUG",
                  backtrace=True,
                  diagnose=True,
                  colorize=True,
                  )
    if not format: del kwargs['format']
    log.add(sys.stdout, **kwargs)
    if format: log.debug(f"{format=}")


@log.catch
def main():
    Tests.test1()
    Tests.test()


if __name__ == '__main__': main()
