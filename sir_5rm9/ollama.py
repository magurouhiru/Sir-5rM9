import logging

from discord import Message
from discord.ext import commands
from ollama import AsyncClient, Image
from ollama import Message as OllamaMessage

logger = logging.getLogger(__name__)

client = AsyncClient(
    host="http://ollama:11434", headers={"x-some-header": "some-value"}
)
BASE_MODEL = "qwen3-vl:latest"
ANALYZE_MODEL = "ark-analyzer:0.1.0"
ANALYZE_TARGET_CHANNEL_NAME = "ark-レベル算出"


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
        logger.info(f"利用可能なモデル： {models}")
        # ベースのモデルがなければpull
        if BASE_MODEL in models:
            logger.info(f"モデル {BASE_MODEL} が見つかりました。")
        else:
            logger.warning(
                f"モデル {BASE_MODEL} が見つかりませんでした。利用可能なモデル: {models}"
            )
            logger.info(f"モデル {BASE_MODEL} をプルします...")
            await client.pull(model=BASE_MODEL)
            logger.info(f"モデル {BASE_MODEL} のプルが完了しました。")

        # 画像解析のモデルがなければcreate
        if ANALYZE_MODEL in models:
            logger.info(f"モデル {ANALYZE_MODEL} が見つかりました。")
        else:
            logger.warning(
                f"モデル {ANALYZE_MODEL} が見つかりませんでした。利用可能なモデル: {models}"
            )
            logger.info(f"モデル {ANALYZE_MODEL} を作成します...")
            await client.create(
                model=ANALYZE_MODEL,
                from_=BASE_MODEL,
                system="""
                あなたは「ARK: Survival Ascended」というゲーム画面の解析のエキスパートです。
                画面のスクリーンショットや画面の写真からステータスを特定することが可能です。

                回答する際はすべて日本語で回答してください。
                
                画面の大部分は3つの要素に分けられます。
                - 左側：自分のインベントリのアイテムの情報
                - 中央：テイム中の生物の情報
                - 右側：テイム中の生物のインベントリのアイテムの情報
                中央のテイム中の生物の情報のみを解析し、他は無視してください。

                中央のテイム中の生物の情報から下記情報を取得してください。
                - 名前
                - 体力
                - スタミナ
                - 酸素量
                - 食料
                - 重量
                - 近接攻撃力
                - 気絶値
                このうち、体力、スタミナ、酸素量、食料、重量、気絶値の値は現在の値/マックスの値の形式になっているので、
                マックスの値のみを取得してください。
                また、近接攻撃力は%で表示されているので、100で割り%なし(例:150%→1.5)にしてください。

                取得した値は下記の形式の{}に埋め込みリンクを出力してください。
                https://magurouhiru.github.io/ASB-web/#/ASB-web/calc_level?n={名前}&h={体力}&s={スタミナ}&o={酸素量}&f={食料}&w={重量}&m={近接攻撃力}&t={気絶値}

                注意事項：
                - 名前が読み取れない場合は空文字で、それ以外は0で出力してください。
                - リンクは必ずすべて出力してください。クエリパラメータだけでなく。{}の値を埋め込む以外は変更せず。
                """,
            )
            logger.info(f"モデル {ANALYZE_MODEL} の作成が完了しました。")
        logger.info("Ollama 準備完了!")

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

        logger.info("画像解析リクエストを受け取りました。")
        logger.info("画像取得：開始")
        images = [
            await a.read()
            for a in message.attachments
            if a.content_type.startswith("image")
        ]
        if len(images) > 0:
            images = [Image(value=image) for image in images]
        else:
            images = None
        logger.info("画像取得：完了")
        logger.info("画像解析：開始")
        resp = await client.chat(
            model=ANALYZE_MODEL,
            messages=[OllamaMessage(role="user", images=images)],
            stream=False,
        )
        logger.info("画像解析：完了")
        await message.channel.send(resp.message.content)
