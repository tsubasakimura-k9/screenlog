"""アクティブウィンドウ取得モジュール"""

import subprocess


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
