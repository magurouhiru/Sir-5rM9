import logging
from typing import List

import aiohttp
from aiohttp import FormData
from discord import Attachment, Message
from discord.ext import commands

logger = logging.getLogger(__name__)

ANALYZE_TARGET_CHANNEL_NAME = "ark-レベル算出"


def setup_ark(bot: commands.Bot):

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

        # FormDataオブジェクトを作成
        data = FormData()
        # "file" はサーバー側が期待するフィールド名
        data.add_field(
            "file",
            await image_attachments[0].read(),
            filename=image_attachments[0].filename,
            content_type=image_attachments[0].content_type,
        )
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:8000/ocr", data=data) as response:
                print("Status:", response.status)
                print("Content-type:", response.headers["content-type"])

                html = await response.text()
                print("Body:", html)
        # resp = ocr_main(image_bytes_list[0])
        # await message.channel.send(
        #     f"https://magurouhiru.github.io/ASB-web/#/ASB-web/calc_level?n={resp['name']}&h={resp['status']['h']}&s={resp['status']['s']}&o={resp['status']['o']}&f={resp['status']['f']}&w={resp['status']['w']}&m={resp['status']['m']}&t={resp['status']['t']}",
        #     silent=True,
        #     mention_author=True,
        # )
