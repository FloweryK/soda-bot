from collections import defaultdict
import discord
from discord.ext import commands
from .. import InterfaceDiscord


class Config:
    def __init__(self):
        self.is_free_chat: bool = False


class General(commands.Cog):
    def __init__(self, bot: InterfaceDiscord):
        self.bot = bot
        self.channels = defaultdict(Config)
    
    @commands.command()
    async def ping(self, ctx: commands.Context[InterfaceDiscord]):
        await ctx.defer(ephemeral=True)
        await ctx.send(f"Pong! ({self.bot.latency * 1000:.2f}ms @{ctx.channel.id})")
    
    @commands.command()
    async def chatstart(self, ctx: commands.Context[InterfaceDiscord]):
        self.channels[ctx.channel.id].is_free_chat = True
        await ctx.send("activated free chat mode!")
    
    @commands.command()
    async def chatend(self, ctx: commands.Context[InterfaceDiscord]):
        self.channels[ctx.channel.id].is_free_chat = False
        await ctx.send("deactivated free chat mode!")
    
    @commands.Cog.listener("on_message")
    async def chat(self, message: discord.Message):
        # Ensure the bot does not respond to itself
        if (message.author == self.bot.user) or message.content.startswith(self.bot.command_prefix):
            return

        if self.channels[message.channel.id].is_free_chat:
            # Process the message (e.g., send a response)
            for s in self.bot.brain.chat(question=message.content, is_stream=False):
                await message.channel.send(f"{s['text']}\n\temotions: {s['emotions']}\n\tcontexts: {s['contexts']}")

    
async def setup(bot: InterfaceDiscord):
    await bot.add_cog(General(bot))