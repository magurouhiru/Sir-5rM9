"""
sir_5rm9: Discord のbot のコア部分を担うモジュール
すべてのコマンドやイベントはこのモジュールを通して登録される。
"""

from .setup_all import setup_all

__all__ = ["setup_all"]
