from logging import Logger
from typing import List

from core.ark import analyze_main
from core.ocr import OCR
from discord import Attachment, Message
from discord.ext import commands

ANALYZE_TARGET_CHANNEL_NAME = "ark-レベル算出"


def setup_ark(bot: commands.Bot, ocr: OCR, logger: Logger):

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
        logger.info(
            "analyze request received. channel: %s, author: %s",
            message.channel.name,
            message.author.name,
        )

        image_attachments: List[Attachment] = [
            a for a in message.attachments if a.content_type.startswith("image")
        ]
        if len(image_attachments) <= 0:
            await message.channel.send("画像がないよう～", silent=True)
            logger.info("analyze request rejected: no image attachment.")
            return

        try:
            resp = await analyze_main(await image_attachments[0].read(), ocr, logger)
            await message.channel.send(
                "".join([
                    "https://magurouhiru.github.io/ASB-web/#/ASB-web/calc?",
                    f"&type={resp.status.type}",
                    f"n={resp.n}",
                    f"&h={resp.status.h}",
                    f"&s={resp.status.s}",
                    f"&o={resp.status.o}",
                    f"&f={resp.status.f}",
                    f"&w={resp.status.w}",
                    f"&m={resp.status.m}",
                    f"&t={resp.status.t}",
                    f"&i={resp.status.i}" if resp.status.i is not None else "",
                    f"&level={resp.status.level}"
                    if resp.status.level is not None
                    else "",
                    f"&level={resp.status.withDom}"
                    if resp.status.withDom is not None
                    else "",
                ]),
                silent=True,
                mention_author=True,
            )
        except Exception as e:
            logger.exception("analyze failed.")
            await message.channel.send(
                f"画像解析に失敗しました。{str(e)}",
                silent=True,
                mention_author=True,
            )
