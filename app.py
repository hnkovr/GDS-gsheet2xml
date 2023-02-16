import heroku_0_init
from main import main
from util import ef, init_logger, logi, logd, bash


@ef
def run():
    logi(f"Starting app!..")
    logd(f"{heroku_0_init.__all__ = }")
    bash("sh app.sh")
    logi(f"App's been started!")


if __name__ == '__main__':
    init_logger()
    run()
    main()
