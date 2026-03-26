from enum import Enum
from typing import Final

APP_ENV: Final[str] = "APP_ENV"
APP_ENV_PRODUCTION: Final[str] = "production"
APP_ENV_DEVELOPMENT: Final[str] = "development"


class AppEnv(Enum):
    PRODUCTION = APP_ENV_PRODUCTION
    DEVELOPMENT = APP_ENV_DEVELOPMENT


DISCORD_TOKEN: Final[str] = "DISCORD_TOKEN"
