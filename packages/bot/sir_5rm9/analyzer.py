import io
import logging
import os
from dataclasses import dataclass

from core import OCRResultList, SearchParams, settings
from PIL import Image

from ocr.ocr import ImageReader

logger = logging.getLogger(__name__)


@dataclass
class Status:
    h: float
    s: float
    o: float
    f: float
    w: float
    m: float
    t: float


@dataclass
class AnalyzeResult:
    n: str
    status: Status


async def analyze_main(image_bytes: bytes, reader: ImageReader) -> AnalyzeResult:
    if settings.dev_mode:
        os.makedirs("ocr_dev", exist_ok=True)
    # 画像取得
    original_image = Image.open(io.BytesIO(image_bytes))
    if settings.dev_mode:
        original_image.save("./ocr_dev/original_image.png")

    # トリミング
    original_width, original_height = original_image.size
    dw = original_height * 0.15
    crop_box = (
        original_width / 2 - dw,
        original_height * 0.1,
        original_width / 2 + dw,
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
    status_crop_box_list = [
        (gray_width / 2, status_start + dh * 0, gray_width, status_start + dh * 1),
        (gray_width / 2, status_start + dh * 1, gray_width, status_start + dh * 2),
        (gray_width / 2, status_start + dh * 2, gray_width, status_start + dh * 3),
        (gray_width / 2, status_start + dh * 3, gray_width, status_start + dh * 4),
        (gray_width / 2, status_start + dh * 4, gray_width, status_start + dh * 5),
        (gray_width / 2, status_start + dh * 5, gray_width, status_start + dh * 6),
        (gray_width / 2, status_start + dh * 6, gray_width, status_start + dh * 7),
    ]
    cropped_status_image_list = [
        final_resized_image.crop(cb) for cb in status_crop_box_list
    ]
    if settings.dev_mode:
        for i, image in enumerate(cropped_status_image_list):
            image.save(f"./ocr_dev/cropped_status_image_{i}.png")

    # テキスト抽出
    ## 名前
    # name_image = np.array(cropped_name_image)
    name_results = await reader.read(
        image=cropped_name_image,
        params=SearchParams(decoder="beamsearch", beamWidth=5),
    )
    if settings.dev_mode:
        for i, nr in enumerate(name_results):
            logging.info(f"name: index: {i}, text: {nr}")

    result = AnalyzeResult(
        n="".join([nr.text for nr in name_results.root]),
        status=await get_status(cropped_status_image_list, reader),
    )
    if settings.dev_mode:
        logging.info(f"result: {result}")
    return result


async def read_status_text(
    image_list: list[Image.Image], allowlist: str, reader: ImageReader
) -> list[OCRResultList]:
    return [
        await reader.read(
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
        for image in image_list
    ]


async def get_status(image_list: list[Image.Image], reader: ImageReader) -> Status:
    # textのみを抽出
    results = await read_status_text(image_list, "0123456789/%.", reader)
    text_list_list = [[r.text for r in result.root] for result in results]
    if settings.dev_mode:
        logging.info(f"text_list_list: {text_list_list}")
    # /が1とかになってる想定で修正する。
    # 1を含めないでテキスト抽出
    tmp_results = await read_status_text(image_list, "023456789/%.", reader)
    tmp_text_list_list = [[r.text for r in result.root] for result in tmp_results]
    if settings.dev_mode:
        logging.info(f"tmp_text_list_list: {tmp_text_list_list}")
    # 返す値のリスト
    value_list: list[str] = []
    for i, tl in enumerate(text_list_list):
        if len(tl) == 0:
            # 酸素量がなくて余るときにここへ来る想定
            continue
        elif len(tl) == 1:
            # 近接攻撃力と/が1とかになってつながってるやつがここへ来る想定
            index = tmp_text_list_list[i][0].find("/")
            if index < 0:
                # /がなければ1個目のやつを入れる
                # 多分近接攻撃力だけのはず
                value_list.append(tl[0])
            else:
                # /の位置以降のやつを入れる
                value_list.append(tl[0][index + 1 :])
        else:
            # うまく/で開業していたらここへ来る想定
            value_list.append(tl[1])

    # /と%を削除
    value_list: list[str] = [v.replace("/", "").replace("%", "") for v in value_list]
    # .がなければ追加
    value_list: list[str] = [
        v if v.find(".") > 0 else v[:-1] + "." + v[-1:] for v in value_list
    ]
    # .の右隣りまで
    for i, v in enumerate(value_list):
        dotindex = v.find(".")
        if dotindex < 0:
            # 上で設定しているので、ここには来ない想定
            continue
        value_list[i] = v[: dotindex + 2]

    if len(value_list) == 7:
        # 全部のステータスが表示されているときにここへ来る想定
        return Status(
            h=float(value_list[0]),
            s=float(value_list[1]),
            o=float(value_list[2]),
            f=float(value_list[3]),
            w=float(value_list[4]),
            m=float(value_list[5]) / 100,
            t=float(value_list[6]),
        )
    else:
        # 酸素量がないときにここへ来る想定
        return Status(
            h=float(value_list[0]),
            s=float(value_list[1]),
            o=float("0"),
            f=float(value_list[2]),
            w=float(value_list[3]),
            m=float(value_list[4]) / 100,
            t=float(value_list[5]),
        )
