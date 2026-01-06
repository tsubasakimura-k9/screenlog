#!/usr/bin/env python3
"""ScreenLog - py2app エントリポイント"""

import sys
import os

# アプリバンドル内のリソースパスを設定
if getattr(sys, 'frozen', False):
    # py2appでビルドされたアプリとして実行されている場合
    app_dir = os.path.dirname(sys.executable)
    # ログ出力先を設定
    log_dir = os.path.expanduser('~/ScreenLog')
    os.makedirs(log_dir, exist_ok=True)

    # stdout/stderrをファイルにリダイレクト（UTF-8エンコーディングを指定）
    sys.stdout = open(os.path.join(log_dir, 'screenlog.log'), 'a', buffering=1, encoding='utf-8')
    sys.stderr = open(os.path.join(log_dir, 'screenlog.error.log'), 'a', buffering=1, encoding='utf-8')

from screenlog.main import main

if __name__ == "__main__":
    main()
