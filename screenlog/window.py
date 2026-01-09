"""アクティブウィンドウ取得モジュール - PyObjC版"""

import gc
from typing import Optional


def get_active_app() -> str:
    """
    アクティブなアプリケーション名を取得（NSWorkspace使用、権限不要）

    Returns:
        str: アプリケーション名。取得失敗時は"Unknown"
    """
    try:
        from AppKit import NSWorkspace

        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.frontmostApplication()

        if active_app:
            return active_app.localizedName() or "Unknown"
        return "Unknown"

    except ImportError:
        print("AppKit not available")
        return "Unknown"
    except Exception as e:
        print(f"Get active app error: {e}")
        return "Unknown"


def get_window_title() -> str:
    """
    アクティブウィンドウのタイトルを取得（AXUIElement使用）

    Returns:
        str: ウィンドウタイトル。取得失敗時は"Unknown"
    """
    try:
        from AppKit import NSWorkspace
        from ApplicationServices import (
            AXUIElementCreateApplication,
            AXUIElementCopyAttributeValue,
            kAXFocusedWindowAttribute,
            kAXTitleAttribute,
        )
        from CoreFoundation import CFRelease

        # アクティブアプリのPIDを取得
        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.frontmostApplication()

        if not active_app:
            return "Unknown"

        pid = active_app.processIdentifier()

        # AXUIElementを作成
        app_element = AXUIElementCreateApplication(pid)
        if not app_element:
            return "Unknown"

        try:
            # フォーカスされているウィンドウを取得
            error, focused_window = AXUIElementCopyAttributeValue(
                app_element, kAXFocusedWindowAttribute, None
            )

            if error or not focused_window:
                return "Unknown"

            try:
                # ウィンドウタイトルを取得
                error, title = AXUIElementCopyAttributeValue(
                    focused_window, kAXTitleAttribute, None
                )

                if error or not title:
                    return "Unknown"

                return str(title)

            finally:
                # focused_windowの参照をクリア
                del focused_window

        finally:
            # app_elementの参照をクリア
            del app_element

    except ImportError as e:
        print(f"Required framework not available: {e}")
        return "Unknown"
    except Exception as e:
        # アクセシビリティ権限がない場合もここに来る
        # エラーメッセージは出さない（頻繁に呼ばれるため）
        return "Unknown"


def get_active_window_info() -> tuple[str, str]:
    """
    アクティブウィンドウの情報を取得

    Returns:
        tuple[str, str]: (アプリケーション名, ウィンドウタイトル)
    """
    return get_active_app(), get_window_title()


def get_active_window_id() -> Optional[int]:
    """
    アクティブウィンドウのウィンドウIDを取得（screencaptureコマンド用）

    Returns:
        Optional[int]: ウィンドウID。取得失敗時はNone
    """
    window_list = None

    try:
        import objc
        import Quartz

        # Autoreleaseプール内で実行してメモリリークを防ぐ
        with objc.autorelease_pool():
            # 最前面のウィンドウを直接取得する方法に変更
            # kCGWindowListOptionOnScreenOnly: 画面に表示されているウィンドウのみ
            window_list = Quartz.CGWindowListCopyWindowInfo(
                Quartz.kCGWindowListOptionOnScreenOnly,
                Quartz.kCGNullWindowID
            )

            if not window_list:
                return None

            # ウィンドウリストは前面から並んでいるので、最初の通常ウィンドウを探す
            for window in window_list:
                owner_name = window.get(Quartz.kCGWindowOwnerName, "")
                window_layer = window.get(Quartz.kCGWindowLayer, -1)
                window_alpha = window.get(Quartz.kCGWindowAlpha, 0)

                # システムUI（Dock, メニューバー等）を除外
                # layer=0 が通常のウィンドウ、alpha>0 が表示されているウィンドウ
                if (window_layer == 0 and
                    window_alpha > 0 and
                    owner_name not in ["Window Server", "Dock"]):
                    window_id = window.get(Quartz.kCGWindowNumber, None)
                    if window_id is not None:
                        return int(window_id)

            return None

    except ImportError:
        print("Quartz framework not available")
        return None
    except Exception as e:
        print(f"Failed to get window ID: {e}")
        return None

    finally:
        # Autoreleaseプールがオブジェクトを解放するため、
        # Python参照のクリアとGCのみ実行
        window_list = None
        gc.collect()
