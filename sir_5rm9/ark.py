import logging

from discord import Message
from discord.ext import commands
from ollama import AsyncClient

from .ocr import ocr_main

logger = logging.getLogger(__name__)

client = AsyncClient(
    host="http://ollama:11434", headers={"x-some-header": "some-value"}
)
BASE_MODEL = "qwen3.5:2b"
# BASE_MODEL = "qwen3.5:0.8b"
# BASE_MODEL = "qwen3-vl:2b"
# BASE_MODEL = "gemma3:latest"
# BASE_MODEL = "glm-ocr:latest"
# BASE_MODEL = "moondream:latest"
ANALYZE_MODEL = f"ark-analyzer_{BASE_MODEL}"
ANALYZE_TARGET_CHANNEL_NAME = "ark-レベル算出"


def setup_ark(bot: commands.Bot):

    @bot.event
    async def on_message(message: Message):
        # 自身のメッセージには反応しない。
        # 指定のチャンネル名以外では反応しない。
        if (
            message.author == bot.user
            or ANALYZE_TARGET_CHANNEL_NAME not in message.channel.name
        ):
            # コマンドがあれば実行できるように渡す。
            await bot.process_commands(message)
            return

        await message.channel.send("画像解析リクエストを受け取りました。", silent=True)
        logger.info("画像解析リクエストを受け取りました。")

        logger.info("画像取得：開始")
        image_bytes_list = [
            await a.read()
            for a in message.attachments
            if a.content_type.startswith("image")
        ]
        if len(image_bytes_list) <= 0:
            return
        logger.info("画像取得：完了")

        logger.info("画像解析：開始")
        resp = ocr_main(image_bytes_list[0])
        logger.info("画像解析：完了")

        message.channel.send(
            f"https://magurouhiru.github.io/ASB-web/#/ASB-web/calc_level?n={resp.name}&h={resp.status.h}&s={resp.status.s}&o={resp.status.o}&f={resp.status.f}&w={resp.status.w}&m={resp.status.m}&t={resp.status.t}",
            silent=True,
        )
