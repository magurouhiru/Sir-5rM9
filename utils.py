# Docker Secretからシークレットを取得する関数
def get_secret(secret_name):
    path = f"/run/secrets/{secret_name}"
    # Docker Secretの標準パスからファイルを読み込む
    with open(path, "r") as f:
        return f.read().strip()
