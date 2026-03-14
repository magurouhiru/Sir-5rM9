from discord.ext import commands

from .logger import log_command


def setup_echo(bot: commands.Bot):
    """
    コマンド: $echo
    説明: メッセージと画像をエコーする(そのまま返す)コマンド
    """

    @bot.command()
    @log_command
    async def echo(ctx: commands.Context, *args: str):
        message = " ".join(args)
        file = None
        if len(ctx.message.attachments) > 0 and ctx.message.attachments[
            0
        ].content_type.startswith("image"):
            file = await ctx.message.attachments[0].to_file()
        await ctx.send(f"Message echoed: {message}", file=file)
