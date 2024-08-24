from dotenv import load_dotenv
load_dotenv('.env')

import config
from interface.discord import InterfaceDiscord


if __name__ == "__main__":
    interface = InterfaceDiscord(config)
    interface.run()