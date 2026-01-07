"""スクリーンキャプチャモジュール"""

import os
from pathlib import Path
from datetime import datetime

import Quartz
from AppKit import NSBitmapImageRep, NSPNGFileType


def get_tmp_dir() -> Path:
    """一時ファイル用ディレクトリを取得"""
    # アプリパッケージ配下のdata/tmpを使用
    tmp_dir = Path(__file__).parent.parent / "data" / "tmp"
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
        # Quartz APIを使用してスクリーンキャプチャ
        if window_id is not None:
            # 特定ウィンドウをキャプチャ
            image = Quartz.CGWindowListCreateImage(
                Quartz.CGRectNull,  # ウィンドウの境界を自動取得
                Quartz.kCGWindowListOptionIncludingWindow,
                window_id,
                Quartz.kCGWindowImageDefault
            )

            # ウィンドウキャプチャが失敗した場合、フルスクリーンにフォールバック
            if image is None:
                image = Quartz.CGWindowListCreateImage(
                    Quartz.CGRectInfinite,
                    Quartz.kCGWindowListOptionOnScreenOnly,
                    Quartz.kCGNullWindowID,
                    Quartz.kCGWindowImageDefault
                )
        else:
            # 画面全体をキャプチャ
            image = Quartz.CGWindowListCreateImage(
                Quartz.CGRectInfinite,
                Quartz.kCGWindowListOptionOnScreenOnly,
                Quartz.kCGNullWindowID,
                Quartz.kCGWindowImageDefault
            )

        if image is None:
            print("Failed to capture screen image")
            return None

        # CGImageをPNGファイルに保存
        bitmap = NSBitmapImageRep.alloc().initWithCGImage_(image)
        if bitmap is None:
            print("Failed to create bitmap from image")
            return None

        png_data = bitmap.representationUsingType_properties_(NSPNGFileType, None)
        if png_data is None:
            print("Failed to create PNG data")
            return None

        png_data.writeToFile_atomically_(str(filepath), True)

        if not filepath.exists():
            print("Screenshot file was not created")
            return None

        return str(filepath)

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
