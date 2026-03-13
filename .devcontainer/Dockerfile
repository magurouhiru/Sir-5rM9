# 公式のDev Containerイメージをベースに使用
# https://github.com/devcontainers/templates/tree/main/src/python
FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

# 定数の定義
ARG USERNAME=vscode \
    WORKSPACE=/home/${USERNAME}/app

# rootだとなんとなく嫌なので、vscodeユーザーに切り替える
USER ${USERNAME}
WORKDIR /home/${USERNAME}

ENV APP_ENV=development \
    POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip3 install --upgrade pip && \
    pip3 install pdoc3 && \
    pipx install poetry==2.3.2
