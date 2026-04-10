from logging import Logger

from core.ocr import builder
from discord.ext import commands

from .ark import setup_ark
from .hello import setup_hello
from .on_ready import setup_on_ready


def setup_all(bot: commands.Bot, logger: Logger):
    """すべてのコマンドやイベントを登録する関数"""
    setup_on_ready(bot, logger)
    setup_hello(bot, logger)
    ocr = builder(logger)
    setup_ark(bot, ocr, logger)
