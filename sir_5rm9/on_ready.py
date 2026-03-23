import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


def setup_on_ready(bot: commands.Bot):

    @bot.event
    async def on_ready():
        logger.info("Sir-5rM9 起動！")
