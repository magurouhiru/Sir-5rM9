# 公式のDev Containerイメージをベースに使用
# https://github.com/devcontainers/templates/tree/main/src/python
FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

# 定数の定義
ARG USERNAME=vscode \
    WORKSPACE=/home/${USERNAME}/app

RUN mkdir -p ${WORKSPACE} && \
    apt-get update && \
    apt-get upgrade -y

# rootだとなんとなく嫌なので、vscodeユーザーに切り替える
USER ${USERNAME}
WORKDIR ${WORKSPACE}

RUN pip3 install --upgrade pip && \
    pipx install uv
