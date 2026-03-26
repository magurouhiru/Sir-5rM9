import io
import logging
import os

import easyocr
import numpy as np
from numpy.typing import NDArray
from PIL import Image

from config.config import APP_ENV, AppEnv

ENV = os.getenv(APP_ENV)

logger = logging.getLogger(__name__)

reader = easyocr.Reader(["ja"], gpu=False)


def ocr_main(image_bytes: bytes):
    # 画像取得
    original_image = Image.open(io.BytesIO(image_bytes))
    if ENV == AppEnv.DEVELOPMENT.value:
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
    if ENV == AppEnv.DEVELOPMENT.value:
        cropped_image.save("./ocr_dev/cropped_image.png")

    # グレースケール変換
    grayscale_image = cropped_image.convert("L")
    if ENV == AppEnv.DEVELOPMENT.value:
        grayscale_image.save("./ocr_dev/grayscale_image.png")

    # 開発用(解析に使うimageを簡単に切り替えられるように)
    final_resized_image = cropped_image
    # final_resized_image = grayscale_image

    # 取得したい場所を個別に取得
    gray_width, gray_height = final_resized_image.size
    ## 名前
    name_crop_box = (0, gray_height * 0.12, gray_width, gray_height * 0.155)
    cropped_name_image = final_resized_image.crop(name_crop_box)
    if ENV == AppEnv.DEVELOPMENT.value:
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
    if ENV == AppEnv.DEVELOPMENT.value:
        for i, image in enumerate(cropped_status_image_list):
            image.save(f"./ocr_dev/cropped_status_image_{i}.png")

    # テキスト抽出
    ## 名前
    name_image = np.array(cropped_name_image)
    name_results = reader.readtext(
        name_image, allowlist=None, decoder="beamsearch", beamWidth=5
    )
    if ENV == AppEnv.DEVELOPMENT.value:
        for i, nr in enumerate(name_results):
            logging.info(f"name: index: {i}, text: {nr[1]}")
    ## ステータス
    status_image_list = [np.array(csi) for csi in cropped_status_image_list]
    status_results_list = read_status_text(status_image_list, "0123456789/%.")
    if ENV == AppEnv.DEVELOPMENT.value:
        for i, srs in enumerate(status_results_list):
            for j, sr in enumerate(srs):
                logging.info(f"status: index: {i} {j}, text: {sr[1]}")

    result = {
        "name": get_name(name_results),
        "status": get_status(status_image_list, status_results_list),
    }
    if ENV == AppEnv.DEVELOPMENT.value:
        logging.info(f"result: {result}")
    return result


def read_status_text(image_list: list[NDArray], allowlist: str):
    return [
        reader.readtext(
            image,
            allowlist=allowlist,
            mag_ratio=1.5,
            contrast_ths=0.05,
            adjust_contrast=0.9,
            text_threshold=0.5,
            low_text=0.2,
            link_threshold=0.3,
        )
        for image in image_list
    ]


def get_name(results: list[list]):
    return "".join([r[1] for r in results])


def get_status(image_list: list[NDArray], results_list: list[list[list]]):
    # textのみを抽出
    text_list_list: list[list[str]] = [[r[1] for r in rs] for rs in results_list]
    if ENV == AppEnv.DEVELOPMENT.value:
        logging.info(f"text_list_list: {text_list_list}")
    # /が1とかになってる想定で修正する。
    # 1を含めないでテキスト抽出
    tmp_results_list = read_status_text(image_list, "023456789/%.")
    tmp_text_list_list: list[list[str]] = [
        [tr[1] for tr in trs] for trs in tmp_results_list
    ]
    if ENV == AppEnv.DEVELOPMENT.value:
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
        return {
            "h": value_list[0],
            "s": value_list[1],
            "o": value_list[2],
            "f": value_list[3],
            "w": value_list[4],
            "m": float(value_list[5]) / 100,
            "t": value_list[6],
        }
    else:
        # 酸素量がないときにここへ来る想定
        return {
            "h": value_list[0],
            "s": value_list[1],
            "o": "0",
            "f": value_list[2],
            "w": value_list[3],
            "m": float(value_list[4]) / 100,
            "t": value_list[5],
        }
