import logging

import discord
import sir_5rm9
from discord.ext import commands
from utils import get_secret


def main():
    # ほんとは環境で変えたいけどDEBUGにしてるとログが多すぎるのでINFOで固定
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.info("Starting Sir-5rM9...")

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="$", intents=intents)

    sir_5rm9.setup_all(bot, logger)

    TOKEN = get_secret("DISCORD_TOKEN")
    bot.run(
        TOKEN,
        root_logger=True,
    )


if __name__ == "__main__":
    main()
