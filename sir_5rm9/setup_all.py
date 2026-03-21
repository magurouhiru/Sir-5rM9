from discord.ext import commands

from .ark import setup_ark
from .echo import setup_echo
from .hello import setup_hello
from .on_ready import setup_on_ready


def setup_all(bot: commands.Bot):
    """すべてのコマンドやイベントを登録する関数"""
    setup_on_ready(bot)
    setup_hello(bot)
    setup_echo(bot)
    # setup_ollama(bot)
    setup_ark(bot)
