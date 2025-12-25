"""アクティブウィンドウ取得モジュール"""

import subprocess
from typing import Optional


def get_active_app() -> str:
    """
    アクティブなアプリケーション名を取得

    Returns:
        str: アプリケーション名。取得失敗時は"Unknown"
    """
    script = '''
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        return name of frontApp
    end tell
    '''

    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Failed to get active app: {result.stderr}")
            return "Unknown"

    except subprocess.TimeoutExpired:
        print("Get active app timed out")
        return "Unknown"
    except Exception as e:
        print(f"Get active app error: {e}")
        return "Unknown"


def get_window_title() -> str:
    """
    アクティブウィンドウのタイトルを取得

    Returns:
        str: ウィンドウタイトル。取得失敗時は"Unknown"
    """
    script = '''
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        tell frontApp
            if (count of windows) > 0 then
                return name of front window
            else
                return ""
            end if
        end tell
    end tell
    '''

    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Failed to get window title: {result.stderr}")
            return "Unknown"

    except subprocess.TimeoutExpired:
        print("Get window title timed out")
        return "Unknown"
    except Exception as e:
        print(f"Get window title error: {e}")
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
    try:
        import Quartz

        # アクティブなアプリケーション名を取得
        active_app = get_active_app()
        if active_app == "Unknown":
            return None

        # すべてのウィンドウ情報を取得
        window_list = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements,
            Quartz.kCGNullWindowID
        )

        # アクティブアプリのウィンドウを探す
        for window in window_list:
            owner_name = window.get(Quartz.kCGWindowOwnerName, "")
            window_layer = window.get(Quartz.kCGWindowLayer, -1)

            # アクティブアプリで、かつメインレイヤー（0）のウィンドウを探す
            if owner_name == active_app and window_layer == 0:
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
