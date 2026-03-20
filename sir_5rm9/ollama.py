import logging

from discord.ext import commands
from ollama import AsyncClient, Image, Message

from .logger import log_command

logger = logging.getLogger(__name__)

client = AsyncClient(
    host="http://ollama:11434", headers={"x-some-header": "some-value"}
)
models: set[str] = set()
BASE_MODEL = "qwen3-vl:latest"
DEFAULT_MODEL = "ark-analyzer"


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
        if BASE_MODEL in models:
            logger.info(f"モデル {BASE_MODEL} が見つかりました。")
        else:
            logger.warning(
                f"モデル {BASE_MODEL} が見つかりませんでした。利用可能なモデル: {models}"
            )
            logger.info(f"モデル {BASE_MODEL} をプルします...")
            await client.pull(model=BASE_MODEL)
            logger.info(f"モデル {BASE_MODEL} のプルが完了しました。")
        await client.create(
            model="ark-analyzer",
            from_="qwen3-vl:latest",
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
            このうち、体力、スタミナ、酸素量、食料、重量の値は現在の値/マックスの値の形式になっているので、
            マックスの値のみを取得してください。
            また、近接攻撃力は%で表示されているので、100で割り%なし(例:150%→1.5)にしてください。

            取得した値は下記の形式の{}に埋め込みリンクを出力してください。
            https://magurouhiru.github.io/ASB-web/#/ASB-web/calc_level?n={名前}&h={体力}&s={スタミナ}&o={酸素量}&f={食料}&w={重量}&m={近接攻撃力}

            注意事項：
            - 名前が読み取れない場合は空文字で、それ以外は0で出力してください。
            """,
        )
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
        resp = await client.pull(model=BASE_MODEL)
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
