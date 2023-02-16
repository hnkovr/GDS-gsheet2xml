import doctest
import os
import sys
from textwrap import shorten
from typing import Optional, Any, Callable

import yaml

USE_LOGURU = True

bash = os.system
logd = logi = print
ef = lambda _: _


# todo?
# ` def run(f):
#     def w(*a, **k):
#         return f(*a, *k)
#     exec(f"{f.__}")
#
# @run
@ef
def init_logger():
    global log, logd, logi, ef
    if not USE_LOGURU:
        import logging
        logging.basicConfig(level=logging.DEBUG)
        log = logging
    else:
        import sys
        from loguru import logger
        log = logger
        logd = log.debug
        ef = log.catch
        log.remove()  # remove any existing handlers
        log.add(sys.stdout,
                # format=format,
                level="DEBUG",
                backtrace=True,
                diagnose=True,
                colorize=True,
                )
    logd = log.debug
    logi = log.info

    (lambda msg: [f(msg) for f in (print, log.info)]
     )(f"# {os.getcwd() = }")


init_logger()


# @log.catch
# def init_loguru():
#     format = None
#     # format = '{time:YY/MM/DD HH:mm:ss} {level.name[0]} "{file.path}", line {line}: {message}'
#
#     log.remove()  # remove any existing handlers
#     kwargs = dict(format=format,
#                   level="DEBUG",
#                   backtrace=True,
#                   diagnose=True,
#                   colorize=True,
#                   )
#     if not format: del kwargs['format']
#     log.add(sys.stdout, **kwargs)
#     if format: log.debug(f"{format=}")


def output_by_all_logging_ways(msg):
    import logging
    print(f"#print: {msg}")
    logging.info(f"#logging: {msg}")
    log.info(f"#logging: {msg}")


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


def fprint(fname, max_len=1111, print=print, no_split=False):
    with open(fname) as f:
        fcontent = f.read()
        print(f"File <{fname}> content:",
              f"{shorten(fcontent, max_len) if len(fcontent) > max_len else fcontent}",
              (f"{'*' * 88}" if not no_split else ''),
              sep='\n'
              )


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




class UnknownArgsForRunThisPy(Exception):
    def __init__(self):
        # super().
        log.critical(f"{UnknownArgsForRunThisPy}: {{{sys.argv[1:]=}}}")


def fwrite(fname, text):
    with open(fname, 'w') as f: f.write(text)


def dedup_lines(fname):
    """
    :param fname:
    :return:
    >>> fname = 'dedup_lines.test.txt' #+SKIP
    >>> fwrite(fname, 'line1\\nline2\\nline2\\nline3\\n')
    >>> fprint(fname, no_split=True)
    >>> dedup_lines(fname)
    >>> fprint(fname, no_split=True)
    >>> os.remove(fname)
    """
    with open(fname, 'r') as r:
        lines = r.readlines()
    res = []
    for l in lines:
        if l not in res: res += l
    with open(fname, 'w') as w:
        # w.flush()
        w.writelines(res)
    return fname


@log.catch
def main():
    if len(sys.argv) >= 2:
        log.info(f"Running <{__file__}> with args: {{{sys.argv[1:]}}}:..")
        if sys.argv[1] == '--dedup_lines':
            fname = sys.argv[2]
            dedup_lines(fname)
        else:
            raise UnknownArgsForRunThisPy
    else:
        log.info(f"No args for <{__file__}>: running tests:..")
        # Tests.test1()
        # Tests.test()
        doctest.testmod()


if __name__ == '__main__': main()
