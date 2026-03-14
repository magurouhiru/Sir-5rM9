# 公式のDev Containerイメージをベースに使用
# https://github.com/devcontainers/templates/tree/main/src/python
FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

# 定数の定義
ARG USERNAME=vscode \
    WORKSPACE=/home/${USERNAME}/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    yq

# rootだとなんとなく嫌なので、vscodeユーザーに切り替える
USER ${USERNAME}
WORKDIR /home/${USERNAME}

ENV APP_ENV=development

RUN pip3 install --upgrade pip && \
    pipx install uv
