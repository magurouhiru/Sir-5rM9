import logging
import os

from config import APP_ENV, AppEnv

logger = logging.getLogger(__name__)


# 環境変数から値を取得する関数
def get_env_variable(var_name):
    return os.getenv(var_name)


# Docker Secretからシークレットを取得する関数
def get_secret(secret_name):
    appEnv = os.getenv(APP_ENV)
    if appEnv == AppEnv.PRODUCTION.value:
        path = f"/run/secrets/{secret_name}"
        # Docker Secretの標準パスからファイルを読み込む
        try:
            with open(path, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.error(f"Secret file not found: {path}")
            raise FileNotFoundError(f"Secret file not found: {path}")
    if appEnv == AppEnv.DEVELOPMENT.value:
        # 開発環境では環境変数から直接取得
        return os.getenv(secret_name)

    logger.error(f"Unknown APP_ENV: {appEnv}")
    raise ValueError(f"Unknown APP_ENV: {appEnv}")
