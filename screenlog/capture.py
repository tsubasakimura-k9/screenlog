"""スクリーンキャプチャモジュール"""

import subprocess
import os
import tempfile
from pathlib import Path
from datetime import datetime


def get_tmp_dir() -> Path:
    """一時ファイル用ディレクトリを取得"""
    tmp_dir = Path.home() / "ScreenLog" / "tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir


def take_screenshot(window_id: int | None = None) -> str | None:
    """
    スクリーンショットを撮影し、一時ファイルのパスを返す

    Args:
        window_id: ウィンドウID。指定された場合はそのウィンドウのみをキャプチャ。
                   Noneの場合は画面全体をキャプチャ。

    Returns:
        str | None: 一時ファイルのパス。失敗した場合はNone
    """
    tmp_dir = get_tmp_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = tmp_dir / f"screenshot_{timestamp}.png"

    try:
        # macOS標準のscreencaptureコマンドを使用
        # -x: 音を鳴らさない
        # -C: カーソルを含めない
        # -l <window-id>: 指定されたウィンドウのみをキャプチャ
        cmd = ["screencapture", "-x", "-C"]

        if window_id is not None:
            cmd.extend(["-l", str(window_id)])

        cmd.append(str(filepath))

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print(f"screencapture failed: {result.stderr}")
            return None

        if not filepath.exists():
            print("Screenshot file was not created")
            return None

        return str(filepath)

    except subprocess.TimeoutExpired:
        print("Screenshot capture timed out")
        return None
    except Exception as e:
        print(f"Screenshot capture error: {e}")
        return None


def delete_screenshot(filepath: str) -> bool:
    """
    一時スクリーンショットファイルを削除

    Args:
        filepath: 削除するファイルのパス

    Returns:
        bool: 削除成功した場合True
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception as e:
        print(f"Failed to delete screenshot: {e}")
        return False
