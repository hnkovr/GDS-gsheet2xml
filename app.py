import logging
import os

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


def log(msg):
    print(f"#print: {msg}")
    logging.info(f"#logging: {msg}")
    # loguru.logger.info(f"#logging: {msg}")


log(f"Starting app!..")

os.system("sh app.sh")

log(f"App's been started!")
