import functools
import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


# ログ用デコレータの定義
def log_command(func):
    @functools.wraps(func)
    async def wrapper(ctx: commands.Context):
        logger.info(
            f"{ctx.command} コマンド実行！ ユーザー: {ctx.author} チャンネル: {ctx.channel}"
        )
        return await func(ctx)

    return wrapper


def setup(bot: commands.Bot):

    @bot.event
    async def on_ready():
        logger.info("Sir-5rM9 起動！")

    """ ここにコマンドを追加していく """

    # 例: $hello コマンド
    @bot.command()
    @log_command
    async def hello(ctx: commands.Context):
        await ctx.send("Hello!")
