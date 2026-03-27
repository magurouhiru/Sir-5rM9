import logging

import discord
from discord.ext import commands

import sir_5rm9
from settings.settings import settings
from utils import get_secret

logger = logging.getLogger(__name__)


def main():
    logger.info(f"settings: {settings.model_dump}")
    if settings.dev_mode:
        logger.setLevel(logging.DEBUG)

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="$", intents=intents)

    sir_5rm9.setup_all(bot)

    TOKEN = get_secret("DISCORD_TOKEN")
    bot.run(
        TOKEN,
        root_logger=True,
        log_level=logging.INFO,  # ほんとは環境で変えたいけどDEBUGにしてるとログが多すぎるのでINFOで固定
    )


if __name__ == "__main__":
    main()
