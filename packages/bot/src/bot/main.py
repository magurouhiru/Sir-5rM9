import logging

import discord
import sir_5rm9
from discord.ext import commands
from google.cloud.logging.handlers import StructuredLogHandler
from utils import get_secret


def main():
    # ほんとは環境で変えたいけどDEBUGにしてるとログが多すぎるのでINFOで固定
    handler = StructuredLogHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info("Starting Sir-5rM9...")

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="$", intents=intents)

    sir_5rm9.setup_all(bot, logger)

    TOKEN = get_secret("DISCORD_TOKEN")
    bot.run(
        TOKEN,
        log_handler=handler,
        log_formatter=formatter,
        log_level=logging.INFO,
        root_logger=True,
    )


if __name__ == "__main__":
    main()
