import functools
import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


def log_command(func):
    """
    コマンドの実行をログに記録するデコレーター
    すべてのコマンド関数にこのデコレーターを適用することで、誰がどのコマンドを実行したかをログに記録できます。
    """

    @functools.wraps(func)
    async def wrapper(ctx: commands.Context, *args):
        logger.info(
            f"{ctx.command}({', '.join(args)}) コマンド実行！ ユーザー: {ctx.author} チャンネル: {ctx.channel}"
        )
        return await func(ctx, *args)

    return wrapper
