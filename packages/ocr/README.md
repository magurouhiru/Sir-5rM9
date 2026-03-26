# Sir-5rM9
Discord のbot です。  
便利な機能を提供します。

## 機能
- [x] 挨拶機能
  - `$hello`で「Hello!」を返す
- [x] ARK OCRで値取得&リンク作成
  - テイム中の画面のスクショをテキストチャンネル`ark-レベル算出`に貼り付けるとリンクを返す

## メモ
- Discord はセキュリティ的にユーザーの画面共有の映像を取得できないようになっている。

## 開発
### 事前準備
当リポジトリはVS Code のdevcontainer の使用が前提です。  
devcontiner を実行すれば開発環境が自動でセットアップされます。  

実行にはトークンが必要です。  
project フォルダのルートに`discord_token.txt`を作成してください。

加えて、Bot の権限設定が必要です。  
下記権限を有効にしてください。
- Message Content Intent
- テキストの権限
  - メッセージを送る

### フレームワーク・ライブラリ
#### [discord.py](https://github.com/Rapptz/discord.py)
Pythonで書かれた、モダンで使いやすく、機能豊富で非同期対応のDiscord用APIラッパー。  

#### [EasyOCR](https://github.com/JaidedAI/EasyOCR)
名前の通り、簡単にOCRが使えるライブラリ。前処理なしの方が精度が良いことも。裏でPyTorchを使っている。

#### [ruff](https://github.com/astral-sh/ruff)
Rustで書かれた、非常に高速なPythonリンターおよびコードフォーマッター。
