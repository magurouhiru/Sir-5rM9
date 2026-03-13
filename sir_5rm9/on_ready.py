import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


def setup_on_ready(bot: commands.Bot):
    """
    イベント: on_ready
    説明:Botが起動して準備ができたときに呼び出されるイベント
    """

    @bot.event
    async def on_ready():
        logger.info("Sir-5rM9 起動！")
