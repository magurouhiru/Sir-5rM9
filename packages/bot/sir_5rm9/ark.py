import logging
from typing import List

from discord import Attachment, Message
from discord.ext import commands

from ocr.ocr import ImageReader

from .analyzer import analyze_main

logger = logging.getLogger(__name__)

ANALYZE_TARGET_CHANNEL_NAME = "ark-レベル算出"


def setup_ark(bot: commands.Bot, reader: ImageReader):

    @bot.event
    async def on_message(message: Message):
        """
        チャンネル名が"ark-レベル算出"に画像を添付して送ったら発火
        複数添付しても最初の1個だけ処理
        """
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

        image_attachments: List[Attachment] = [
            a for a in message.attachments if a.content_type.startswith("image")
        ]
        if len(image_attachments) <= 0:
            await message.channel.send("画像がないよう～", silent=True)
            logger.info("画像なしで終了。")
            return

        resp = await analyze_main(image_attachments[0], reader)
        await message.channel.send(
            f"https://magurouhiru.github.io/ASB-web/#/ASB-web/calc_level?n={resp.n}&h={resp.status.h}&s={resp.status.s}&o={resp.status.o}&f={resp.status.f}&w={resp.status.w}&m={resp.status.m}&t={resp.status.t}",
            silent=True,
            mention_author=True,
        )
