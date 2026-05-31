import io
import os
from dataclasses import dataclass
from logging import Logger

from api import OCRResultList, SearchParams
from PIL import Image
from typing_extensions import Literal

from core import settings
from core.ocr import OCR


@dataclass
class Status:
    type: Literal["wild", "dom", "bred"]
    h: float
    s: float
    o: float
    f: float
    w: float
    m: float
    t: float
    i: float | None = None


@dataclass
class AnalyzeResult:
    n: str
    status: Status


async def analyze_main(image_bytes: bytes, ocr: OCR, logger: Logger) -> AnalyzeResult:
    if settings.dev_mode:
        os.makedirs("ocr_dev", exist_ok=True)
    # 画像取得
    original_image = Image.open(io.BytesIO(image_bytes))
    if settings.dev_mode:
        original_image.save("./ocr_dev/original_image.png")

    # トリミング
    original_width, original_height = original_image.size
    dl = original_height * 0.1523
    dr = original_height * 0.17
    crop_box = (
        original_width / 2 - dl,
        original_height * 0.1,
        original_width / 2 + dr,
        original_height * 0.7,
    )
    cropped_image = original_image.crop(crop_box)
    if settings.dev_mode:
        cropped_image.save("./ocr_dev/cropped_image.png")

    # グレースケール変換
    grayscale_image = cropped_image.convert("L")
    if settings.dev_mode:
        grayscale_image.save("./ocr_dev/grayscale_image.png")

    # 開発用(解析に使うimageを簡単に切り替えられるように)
    final_resized_image = cropped_image
    # final_resized_image = grayscale_image

    # 取得したい場所を個別に取得
    gray_width, gray_height = final_resized_image.size
    ## 名前
    name_crop_box = (0, gray_height * 0.12, gray_width, gray_height * 0.155)
    cropped_name_image = final_resized_image.crop(name_crop_box)
    if settings.dev_mode:
        cropped_name_image.save("./ocr_dev/cropped_name_image.png")
    ## ステータス
    status_start = gray_height * 0.53
    dh = gray_height * 0.053
    split = 1 / 3
    status_name_crop_box_list = [
        (0, status_start + dh * 0, gray_width * split, status_start + dh * 1),
        (0, status_start + dh * 1, gray_width * split, status_start + dh * 2),
        (0, status_start + dh * 2, gray_width * split, status_start + dh * 3),
        (0, status_start + dh * 3, gray_width * split, status_start + dh * 4),
        (0, status_start + dh * 4, gray_width * split, status_start + dh * 5),
        (0, status_start + dh * 5, gray_width * split, status_start + dh * 6),
        (0, status_start + dh * 6, gray_width * split, status_start + dh * 7),
        (0, status_start + dh * 7, gray_width * split, status_start + dh * 8),
        (0, status_start + dh * 8, gray_width * split, status_start + dh * 9),
    ]
    status_value_crop_box_list = [
        (gray_width * split, status_start + dh * 0, gray_width, status_start + dh * 1),
        (gray_width * split, status_start + dh * 1, gray_width, status_start + dh * 2),
        (gray_width * split, status_start + dh * 2, gray_width, status_start + dh * 3),
        (gray_width * split, status_start + dh * 3, gray_width, status_start + dh * 4),
        (gray_width * split, status_start + dh * 4, gray_width, status_start + dh * 5),
        (gray_width * split, status_start + dh * 5, gray_width, status_start + dh * 6),
        (gray_width * split, status_start + dh * 6, gray_width, status_start + dh * 7),
        (gray_width * split, status_start + dh * 7, gray_width, status_start + dh * 8),
        (gray_width * split, status_start + dh * 8, gray_width, status_start + dh * 9),
    ]
    cropped_status_name_image_list = [
        final_resized_image.crop(cb) for cb in status_name_crop_box_list
    ]
    cropped_status_value_image_list = [
        final_resized_image.crop(cb) for cb in status_value_crop_box_list
    ]
    if settings.dev_mode:
        for i, image in enumerate(cropped_status_name_image_list):
            image.save(f"./ocr_dev/cropped_status_name_image_{i}.png")
    if settings.dev_mode:
        for i, image in enumerate(cropped_status_value_image_list):
            image.save(f"./ocr_dev/cropped_status_image_{i}.png")

    # テキスト抽出
    ## 名前
    # name_image = np.array(cropped_name_image)
    name_results = await ocr.read(
        image=cropped_name_image,
        params=SearchParams(decoder="beamsearch", beamWidth=5),
    )
    if settings.dev_mode:
        for i, nr in enumerate(name_results):
            logger.info(f"name: index: {i}, text: {nr}")

    result = AnalyzeResult(
        n=adjast_name(name_results),
        status=await get_status(
            cropped_status_name_image_list, cropped_status_value_image_list, ocr, logger
        ),
    )
    if settings.dev_mode:
        logger.info(f"result: {result}")
    return result


# クエリパラメータにスペースが入ることがあるので、それを削除するためのリスト
delete_str_list = [" ", "　"]


def adjast_name(result: OCRResultList) -> str:
    name = "".join([r.text for r in result.root])
    for delete_str in delete_str_list:
        name = name.replace(delete_str, "")
    return name.strip()


status_name_dict = {
    "h": "体力",
    "s": "スタミナ",
    "o": "酸素量",
    "f": "食料",
    "w": "重量",
    "m": "近接攻撃力",
    "t": "気絶値",
    "i": "刷り込み中",
}


async def read_status_name_text(image: Image.Image, ocr: OCR) -> str:
    text = ""
    max_confidence = 0.0
    for key, value in status_name_dict.items():
        result = await ocr.read(
            image=image,
            params=SearchParams(allowlist=value, decoder="beamsearch", beamWidth=5),
        )
        if (
            len(result.root) > 0
            and result.root[0].text == value
            and result.root[0].confidence > max_confidence
        ):
            text = key
            max_confidence = result.root[0].confidence
    return text


async def read_status_value_text(
    image: Image.Image, allowlist: str, ocr: OCR
) -> OCRResultList:
    result = await ocr.read(
        image=image,
        params=SearchParams(
            allowlist=allowlist,
            mag_ratio=1.5,
            contrast_ths=0.05,
            adjust_contrast=0.9,
            text_threshold=0.5,
            low_text=0.2,
            link_threshold=0.3,
        ),
    )
    return result


async def get_status(
    status_name_images: list[Image.Image],
    status_value_images: list[Image.Image],
    ocr: OCR,
    logger: Logger,
) -> Status:
    # ステータスの名前をOCRで読み取る
    status_name_list = [
        await read_status_name_text(image, ocr) for image in status_name_images
    ]
    status_type = adjast_status_name_list(status_name_list)
    match status_type:
        case "tb":
            return Status(
                type="wild",
                h=await get_status_value(status_value_images[0], ocr),
                s=await get_status_value(status_value_images[1], ocr),
                o=await get_status_value(status_value_images[2], ocr),
                f=await get_status_value(status_value_images[3], ocr),
                w=await get_status_value(status_value_images[4], ocr),
                m=await get_status_value_m(status_value_images[5], ocr),
                t=await get_status_value(status_value_images[6], ocr),
                i=None,
            )
        case "tbno":
            return Status(
                type="wild",
                h=await get_status_value(status_value_images[0], ocr),
                s=await get_status_value(status_value_images[1], ocr),
                o=0.0,
                f=await get_status_value(status_value_images[2], ocr),
                w=await get_status_value(status_value_images[3], ocr),
                m=await get_status_value_m(status_value_images[4], ocr),
                t=await get_status_value(status_value_images[5], ocr),
                i=None,
            )
        case "ta":
            return Status(
                type="dom",
                h=await get_status_value(status_value_images[1], ocr),
                s=await get_status_value(status_value_images[2], ocr),
                o=await get_status_value(status_value_images[3], ocr),
                f=await get_status_value(status_value_images[4], ocr),
                w=await get_status_value(status_value_images[5], ocr),
                m=await get_status_value_m(status_value_images[6], ocr),
                t=await get_status_value(status_value_images[7], ocr),
                i=None,
            )
        case "tano":
            return Status(
                type="dom",
                h=await get_status_value(status_value_images[1], ocr),
                s=await get_status_value(status_value_images[2], ocr),
                o=0.0,
                f=await get_status_value(status_value_images[3], ocr),
                w=await get_status_value(status_value_images[4], ocr),
                m=await get_status_value_m(status_value_images[5], ocr),
                t=await get_status_value(status_value_images[6], ocr),
                i=None,
            )
        case "bl":
            return Status(
                type="bred",
                h=await get_status_value(status_value_images[1], ocr),
                s=await get_status_value(status_value_images[2], ocr),
                o=await get_status_value(status_value_images[3], ocr),
                f=await get_status_value(status_value_images[4], ocr),
                w=await get_status_value(status_value_images[5], ocr),
                m=await get_status_value_m(status_value_images[6], ocr),
                t=await get_status_value(status_value_images[7], ocr),
                i=await get_status_value_i(status_value_images[8], ocr),
            )
        case "blno":
            return Status(
                type="bred",
                h=await get_status_value(status_value_images[1], ocr),
                s=await get_status_value(status_value_images[2], ocr),
                o=0.0,
                f=await get_status_value(status_value_images[3], ocr),
                w=await get_status_value(status_value_images[4], ocr),
                m=await get_status_value_m(status_value_images[5], ocr),
                t=await get_status_value(status_value_images[6], ocr),
                i=await get_status_value_i(status_value_images[7], ocr),
            )


allow_status_name_list_dict = {
    "tb": ["h", "s", "o", "f", "w", "m", "t", "", ""],  # テイム前
    "tbno": ["h", "s", "f", "w", "m", "t", "", "", ""],  # テイム前かつ酸素量なし
    "ta": ["", "h", "s", "o", "f", "w", "m", "t", ""],  # テイム後
    "tano": ["", "h", "s", "f", "w", "m", "t", "", ""],  # テイム後かつ酸素量なし
    "bl": ["", "h", "s", "o", "f", "w", "m", "t", "i"],  # ブリ
    "blno": ["", "h", "s", "f", "w", "m", "t", "i", ""],  # ブリかつ酸素量なし
}


def adjast_status_name_list(status_name_list: list[str]) -> list[str]:
    # ステータスの名前のリストを、status_name_dictのkeyのリストに変換する
    # 変換できないものは空文字にする
    for type, allow_status_name_list in allow_status_name_list_dict.items():
        flag = True
        for i in range(len(allow_status_name_list)):
            # 空文字か同じならOK
            if (
                status_name_list[i] == ""
                or status_name_list[i] == allow_status_name_list[i]
                or i
                == 0  # テイム後 or ブリで最初が変な感じになることがあるっぽいので、最初は無視する
            ):
                continue
            else:
                flag = False
                break
        if flag:
            return type
    raise ValueError(
        f"酸素のあるなしはOKだけど、それ以外に足りないやつがある or そもそも読み取れないので解析できないぽ。status_name_list: {status_name_list}"
    )


async def get_status_value(image: Image.Image, ocr: OCR) -> float:
    # ステータスの値をOCRで読み取る
    result = await read_status_value_text(image, allowlist="0123456789./", ocr=ocr)
    buf1 = ""
    if len(result.root) == 0:
        raise ValueError("ステータスの値が読み取れないぽ")
    elif len(result.root) == 1:
        # /が1とかになってつながってるやつがここへ来る想定
        tmp_result = await read_status_value_text(
            image, allowlist="023456789./", ocr=ocr
        )
        index = tmp_result.root[0].text.find("/")
        buf1 = result.root[0].text[index + 1 :]
    else:
        # うまく/で開業していたらここへ来る想定
        buf1 = result.root[1].text

    # 念のため/を削除
    buf2 = buf1.replace("/", "")
    buf3 = add_dot_if_needed(buf2)

    return round(float(buf3), 1)


async def get_status_value_m(image: Image.Image, ocr: OCR) -> float:
    # ステータスの値をOCRで読み取る
    result = await read_status_value_text(image, allowlist="0123456789.%", ocr=ocr)
    buf1 = ""
    if len(result.root) == 0:
        raise ValueError("ステータスの値が読み取れないぽ")
    else:
        buf1 = result.root[0].text

    # %を削除
    buf2 = buf1.replace("%", "")
    buf3 = add_dot_if_needed(buf2)

    return round(float(buf3) / 100.0, 3)


async def get_status_value_i(image: Image.Image, ocr: OCR) -> float:
    # ステータスの値をOCRで読み取る
    result = await read_status_value_text(image, allowlist="0123456789%", ocr=ocr)
    print(f"i result: {result}")
    buf1 = ""
    if len(result.root) == 0:
        raise ValueError("ステータスの値が読み取れないぽ")
    else:
        buf1 = result.root[0].text

    # %を削除
    buf2 = buf1.replace("%", "")
    buf3 = int(buf2)
    if buf3 > 199:
        buf3 = buf3 // 10  # なんか%が9とかになるっぽいので、10で割る

    print(f"i buf3: {buf3}")
    return min(100, int(buf3)) / 100.0  # 100%を1.0として扱う


def add_dot_if_needed(value: str) -> str:
    # .がなければ追加(.が読み取れない場合を想定)
    if value.find(".") < 0:
        value = value[:-1] + "." + value[-1:]
    return value
