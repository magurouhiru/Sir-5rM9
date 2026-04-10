from logging import Logger

from core import settings
from discord.ext import commands


def setup_on_ready(bot: commands.Bot, logger: Logger):

    @bot.event
    async def on_ready():
        logger.info("Sir-5rM9 is ready!")
        logger.info(f"settings: {settings.model_dump()}")
