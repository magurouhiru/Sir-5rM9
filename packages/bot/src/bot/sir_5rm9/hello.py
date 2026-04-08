from logging import Logger

from discord.ext import commands


def setup_hello(bot: commands.Bot, logger: Logger):

    @bot.command()
    async def hello(ctx: commands.Context):
        """
        コマンド: $hello
        説明: "Hello!" と返信するコマンド
        """
        logger.info(f"Received command: {ctx.message.content} from {ctx.author}")
        await ctx.send("Hello!", silent=True, mention_author=True)
