import os, logging
from loguru import logger as log
(lambda msg: [f(msg) for f in (print, log.info)]
 )(f"# {os.getcwd() = }")

@log.catch
def init():
    logging.basicConfig(level=logging.DEBUG)
    # import sys, loguru
    # logu = loguru.logger
    # logu.remove()  # remove any existing handlers
    # logu.add(sys.stdout,
    #          # format=format,
    #          level="DEBUG",
    #          backtrace=True,
    #          diagnose=True,
    #          colorize=True,
    #          )


def logi(msg):
    print(f"#print: {msg}")
    logging.info(f"#logging: {msg}")
    log.info(f"#logging: {msg}")

@log.catch
def run():
    logi(f"Starting app!..")

    # from heroku_0_init import final_state
    from heroku_0_init import __all__
    log.debug(f"{__all__ = }")

    os.system("sh app.sh")

    logi(f"App's been started!")

if __name__ == '__main__':
    init()
    run()