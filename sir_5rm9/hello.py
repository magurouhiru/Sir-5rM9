from discord.ext import commands

from .logger import log_command


def setup_hello(bot: commands.Bot):
    """
    コマンド: $hello
    説明: "Hello!" と返信するコマンド
    """

    @bot.command()
    @log_command
    async def hello(ctx: commands.Context):
        await ctx.send("Hello!")
