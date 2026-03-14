import logging

from discord.ext import commands
from ollama import AsyncClient, Image, Message

from .logger import log_command

logger = logging.getLogger(__name__)

client = AsyncClient(
    host="http://ollama:11434", headers={"x-some-header": "some-value"}
)
models: set[str] = set()
DEFAULT_MODEL = "gemma3:latest"


def setup_ollama(bot: commands.Bot):
    """
    コマンド: $ollama
    説明: Ollamaと連携するコマンド
    """

    @bot.event
    async def on_ready():
        logger.info("Ollama 準備開始!")
        logger.info("Ollama モデルの確認!")
        resp = await client.list()
        models = {m.model for m in resp.models if m.model is not None}
        if DEFAULT_MODEL in models:
            logger.info(f"モデル {DEFAULT_MODEL} が見つかりました。")
        else:
            logger.warning(
                f"モデル {DEFAULT_MODEL} が見つかりませんでした。利用可能なモデル: {models}"
            )
            logger.info(f"モデル {DEFAULT_MODEL} をプルします...")
            await client.pull(model=DEFAULT_MODEL)
            logger.info(f"モデル {DEFAULT_MODEL} のプルが完了しました。")
        logger.info("Ollama 準備完了!")

    @bot.command()
    @log_command
    async def ollama_list(ctx: commands.Context):
        resp = await client.list()
        models = {m.model for m in resp.models if m.model is not None}
        await ctx.send(f"Ollama models: {models}")

    @bot.command()
    @log_command
    async def ollama_pull(ctx: commands.Context):
        resp = await client.pull(model=DEFAULT_MODEL)
        await ctx.send(f"Ollama models: {resp}")

    @bot.command()
    @log_command
    async def ollama_chat(ctx: commands.Context, *args: str):
        message = " ".join(args)
        images = [
            await a.read()
            for a in ctx.message.attachments
            if a.content_type.startswith("image")
        ]
        if len(images) > 0:
            images = [Image(value=image) for image in images]
        else:
            images = None
        resp = await client.chat(
            model=DEFAULT_MODEL,
            messages=[Message(role="user", content=message, images=images)],
            stream=False,
        )
        await ctx.send(f"Ollama: {resp.message.content}")
