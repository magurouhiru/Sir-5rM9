from discord.ext import commands

from .logger import log_command


def setup_hello(bot: commands.Bot):

    @bot.command()
    @log_command
    async def hello(ctx: commands.Context):
        """
        コマンド: $hello
        説明: "Hello!" と返信するコマンド
        """
        await ctx.send("Hello!", silent=True, mention_author=True)
