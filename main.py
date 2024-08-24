
from dotenv import load_dotenv
load_dotenv('.env')

import config
from interface.cli import InterfaceCLI


if __name__ == "__main__":
    interface = InterfaceCLI(config)
    interface.run()