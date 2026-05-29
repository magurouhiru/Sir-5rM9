import asyncio
import io
import logging

from core.ark import analyze_main
from core.ark.analyzer import Status
from core.ocr import builder
from PIL import Image

# image_path = "sample.png"  # tb:テイム前
# image_path = "sample2.png"  # bl:ブリ
# image_path = "sample3.jpg"  # tano:テイム後かつ酸素量なし
# image_path = "sample4.png"  # bl:ブリ
# image_path = "sample5.png"  # tbno:テイム前かつ酸素量なし
# image_path = "sample6.png"  # bl:ブリかつ酸素量なし(50%)

sample_list = [
    {
        "name": "sample 雪フクロウ (tb:テイム前) ",
        "path": "sample.png",
        "status": Status(
            type="wild",
            h=2015.0,
            s=1225.0,
            o=510.0,
            f=6200.0,
            w=562.5,
            m=1.9,
            t=5604.0,
            i=None,
        ),
    },
    {
        "name": "sample2 テリジノ (bl:ブリ) ",
        "path": "sample2.png",
        "status": Status(
            type="bred",
            h=8038.9,
            s=1170.0,
            o=480.0,
            f=12960.0,
            w=692.4,
            m=6.366,
            t=11433.5,
            i=100,
        ),
    },
    {
        "name": "sample3 メガロドン (tano:テイム後かつ酸素量なし) ",
        "path": "sample3.jpg",
        "status": Status(
            type="dom",
            h=5760.0,
            s=1696.0,
            o=0.0,
            f=12419.9,
            w=465.0,
            m=4.281,
            t=11504.5,
            i=None,
        ),
    },
    {
        "name": "sample4 ファイアーワイバーン (bl:ブリ) ",
        "path": "sample4.png",
        "status": Status(
            type="bred",
            h=3566.2,
            s=567.0,
            o=390.0,
            f=4320.0,
            w=512.0,
            m=1.882,
            t=4597.0,
            i=100,
        ),
    },
    {
        "name": "sample5 カニ (tbno:テイム前かつ酸素量なし) ",
        "path": "sample5.png",
        "status": Status(
            type="wild",
            h=9600.0,
            s=2040.0,
            o=0.0,
            f=14500.0,
            w=1296.0,
            m=2.5,
            t=6360.0,
            i=None,
        ),
    },
    {
        "name": "sample6 メイグアナ (bl:ブリかつ酸素量なし(50%)) ",
        "path": "sample6.png",
        "status": Status(
            type="bred",
            h=3780.7,
            s=1215.0,
            o=0.0,
            f=10800.0,
            w=704.0,
            m=3.175,
            t=1306.5,
            i=50,
        ),
    },
]


async def main():
    for sample in sample_list:
        result = await test(sample["path"])
        compere = compere_status(result.status, sample["status"])
        if compere is not None:
            raise ValueError(f"{sample['name']}: {compere}")
        print(f"sample: {sample['name']}, result: {result}")


async def test(image_path: str):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    ocr = builder(logger)
    img = Image.open(image_path)

    # 1. メモリ上にバイナリを置くためのバッファを作成
    img_bytes_io = io.BytesIO()

    # 2. バッファに対して画像を保存（フォーマットの指定が必要）
    img.save(img_bytes_io, format="PNG")

    # 3. バッファの中身を bytes として取り出す
    img_bytes = img_bytes_io.getvalue()

    result = await analyze_main(img_bytes, ocr, logger)
    return result


def compere_status(status1: Status, status2: Status) -> None | str:
    if status1.h != status2.h:
        return f"h: {status1.h} != {status2.h}"
    if status1.s != status2.s:
        return f"s: {status1.s} != {status2.s}"
    if status1.o != status2.o:
        return f"o: {status1.o} != {status2.o}"
    if status1.f != status2.f:
        return f"f: {status1.f} != {status2.f}"
    if status1.w != status2.w:
        return f"w: {status1.w} != {status2.w}"
    if status1.m != status2.m:
        return f"m: {status1.m} != {status2.m}"
    if status1.t != status2.t:
        return f"t: {status1.t} != {status2.t}"
    if status1.i != status2.i:
        return f"i: {status1.i} != {status2.i}"
    if status1.type != status2.type:
        return f"type: {status1.type} != {status2.type}"
    return None


if __name__ == "__main__":
    asyncio.run(main())
