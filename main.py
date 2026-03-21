import logging
import os

import discord
from discord.ext import commands

import sir_5rm9
from config.config import APP_ENV, DISCORD_TOKEN, AppEnv
from utils import get_secret

logger = logging.getLogger(__name__)


def main():
    ENV = os.getenv(APP_ENV)

    if ENV == AppEnv.DEVELOPMENT.value:
        logger.setLevel(logging.DEBUG)

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="$", intents=intents)

    sir_5rm9.setup_all(bot)

    TOKEN = get_secret(DISCORD_TOKEN)
    bot.run(
        TOKEN,
        root_logger=True,
        log_level=logging.INFO,  # ほんとは環境で変えたいけどDEBUGにしてるとログが多すぎるのでINFOで固定
    )


if __name__ == "__main__":
    main()
