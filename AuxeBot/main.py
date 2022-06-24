import os
import logging
from Bot import AuxeBot

logger = logging.getLogger(__name__)

print(
    """         .d888888                              888888ba             dP   \n        d8'    88                              88    `8b            88   \n        88aaaaa88a dP    dP dP.  .dP .d8888b. a88aaaa8P' .d8888b. d8888P \n        88     88  88    88  `8bd8'  88ooood8  88   `8b. 88'  `88   88   \n        88     88  88.  .88  .d88b.  88.  ...  88    .88 88.  .88   88   \n        88     88  `88888P' dP'  `dP `88888P'  88888888P `88888P'   dP   \n                          Ascii art by patorjk.com                       """
)

logger.info("Imported modules.")
logger.info("Getting client...")

try:
    import sys
    sys.path.insert(0, os.environ["disutils_path"])
    import disutils
except ImportError or KeyError:
    pass

bot = AuxeBot()

try:
    assert bot.testing
    import inputimeout
    level = inputimeout.inputimeout(
        "Do you want to set logging level to DEBUG (y/n): ", timeout=3
    )
    assert level.lower() == "y"
    level = logging.DEBUG
except AssertionError or ImportError or inputimeout.TimeoutOccurred:
    level = logging.INFO
finally:
    logging.basicConfig(level=level)


if __name__ == "__main__":
    bot.run()

"""
# test run always restart
import os
while True: 
    try:
        print('\n'*100); os.system("py AuxeBot/main.py");
    except KeyboardInterrupt:
        input()
    except:
        pass
"""
