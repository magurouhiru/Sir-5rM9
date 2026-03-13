Module sir_5rm9
===============
sir_5rm9: Discord のbot のコア部分を担うモジュール
すべてのコマンドやイベントはこのモジュールを通して登録される。

Sub-modules
-----------
* sir_5rm9.hello
* sir_5rm9.logger
* sir_5rm9.on_ready

Functions
---------

`setup_all(bot: discord.ext.commands.bot.Bot)`
:   すべてのコマンドやイベントを登録する関数