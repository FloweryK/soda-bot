
from dotenv import load_dotenv
load_dotenv('.env')

import interface.cli
import config


if __name__ == "__main__":
    interface.cli.run(config)