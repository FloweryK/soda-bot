import os
import logging
import discord
from discord.ext import commands
from core.brain import Brain
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")


class InterfaceDiscord(commands.Bot):
    def __init__(self, config, *args, **kwargs):
        self.brain = Brain(
            config.BRAIN_LLM,
            config.BRAIN_NAME, 
            config.BRAIN_PROMPT,
            config.BRAIN_EMOTIONS,
            config.MEMORY_SAVE_DIR,
            config.MEMORY_SHORT_TERM_LIMIT
        )

        # discord initialize
        self.cog_dir: str = config.DISCORD_COG_DIR
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(*args, **kwargs, command_prefix=config.DISCORD_PREFIX, intents=intents)

        # logger
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def _load_extensions(self):
        for filename in os.listdir(self.cog_dir.replace('.', os.path.sep)):
            if filename.endswith('.py') and not filename.startswith('_'):
                await self.load_extension(name=f".{filename[:-3]}", package=self.cog_dir)

    async def on_ready(self) -> None:
        self.logger.info(f"Logged in as {self.user} ({self.user.id})")
    
    async def setup_hook(self):
        await self._load_extensions()
    
    def run(self):
        super().run(os.environ['DISCORD_BOT_TOKEN'])