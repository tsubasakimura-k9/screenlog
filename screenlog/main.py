#!/usr/bin/env python3
"""ScreenLog - メインエントリーポイント"""

import signal
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path

# launchdからの実行時に出力をバッファリングしないようにする
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

from .capture import take_screenshot, delete_screenshot
from .window import get_active_window_info
from .ocr import extract_text
from .logger import create_log_entry, write_log_entry, cleanup_old_logs


# グローバルな停止フラグ
running = True


def signal_handler(signum, frame):
    """シグナルハンドラ（SIGINT, SIGTERM）"""
    global running
    print("\nStopping ScreenLog...")
    running = False


def process_single_capture() -> bool:
    """
    1回のキャプチャ処理を実行

    Returns:
        bool: 処理成功した場合True
    """
    timestamp = datetime.now()

    # 1. スクリーンショットを撮影
    screenshot_path = take_screenshot()
    if screenshot_path is None:
        print(f"[{timestamp.isoformat()}] Screenshot capture failed, skipping...")
        return False

    try:
        # 2. アクティブウィンドウ情報を取得
        active_app, window_title = get_active_window_info()

        # 3. OCR処理
        ocr_result = extract_text(screenshot_path)

        # 4. ログエントリを作成
        entry = create_log_entry(
            active_app=active_app,
            window_title=window_title,
            ocr_text=ocr_result.text,
            ocr_confidence=ocr_result.confidence,
            timestamp=timestamp
        )

        # 5. ログを保存
        success = write_log_entry(entry)

        if success:
            text_preview = ocr_result.text[:50].replace('\n', ' ') if ocr_result.text else "(empty)"
            print(f"[{timestamp.strftime('%H:%M:%S')}] {active_app} - {window_title[:30]}... | OCR: {text_preview}...")
        else:
            print(f"[{timestamp.isoformat()}] Failed to write log entry")

        return success

    finally:
        # 6. 一時ファイルを削除
        delete_screenshot(screenshot_path)


def run_loop(interval: int = 60, retention_days: int = 30):
    """
    メインループを実行

    Args:
        interval: キャプチャ間隔（秒）
        retention_days: ログ保持日数
    """
    global running

    print(f"ScreenLog started. Capturing every {interval} seconds.")
    print(f"Log retention: {retention_days} days")
    print(f"Logs will be saved to: {Path.home() / 'ScreenLog' / 'logs'}")
    print("-" * 60)

    # 起動時に古いログをクリーンアップ
    deleted = cleanup_old_logs(days=retention_days)
    if deleted > 0:
        print(f"Cleaned up {deleted} old log file(s)")

    while running:
        try:
            process_single_capture()

            # 次のキャプチャまで待機（1秒ずつ確認して停止フラグをチェック）
            for _ in range(interval):
                if not running:
                    break
                time.sleep(1)

        except Exception as e:
            print(f"Error in main loop: {e}")
            # エラーが発生しても継続
            time.sleep(interval)

    print("ScreenLog stopped.")


def main():
    """メインエントリーポイント"""
    parser = argparse.ArgumentParser(
        description="ScreenLog - 作業ログ自動生成ツール"
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=60,
        help="キャプチャ間隔（秒）。デフォルト: 60"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="1回だけキャプチャして終了"
    )
    parser.add_argument(
        "-r", "--retention",
        type=int,
        default=30,
        help="ログ保持日数。デフォルト: 30"
    )

    args = parser.parse_args()

    # シグナルハンドラを設定
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if args.once:
        # 1回だけ実行
        success = process_single_capture()
        sys.exit(0 if success else 1)
    else:
        # ループ実行
        run_loop(interval=args.interval, retention_days=args.retention)


if __name__ == "__main__":
    main()
