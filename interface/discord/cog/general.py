from discord.ext import commands
from .. import InterfaceDiscord


class General(commands.Cog):
    def __init__(self, bot: InterfaceDiscord):
        self.bot = bot
    
    @commands.command(name="ping")
    async def add(self, ctx: commands.Context[InterfaceDiscord]):
        await ctx.defer(ephemeral=True)
        await ctx.send(f"Pong! ({self.bot.latency * 1000:.2f}ms)")

    
async def setup(bot: InterfaceDiscord):
    await bot.add_cog(General(bot))