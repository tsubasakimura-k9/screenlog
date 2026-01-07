"""ログ保存モジュール"""

import json
from pathlib import Path
from datetime import datetime
from typing import TypedDict


class LogEntry(TypedDict):
    """圧縮されたログエントリの型定義"""
    start_time: str
    end_time: str
    duration_minutes: int
    snapshot_count: int
    active_app: str
    window_title: str
    ocr_text: str
    avg_ocr_confidence: float | None


def get_log_dir() -> Path:
    """ログディレクトリを取得"""
    # アプリパッケージ配下のdata/logsを使用
    log_dir = Path(__file__).parent.parent / "data" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def get_log_file_path(date: datetime | None = None) -> Path:
    """
    ログファイルのパスを取得

    Args:
        date: 対象日付。Noneの場合は今日

    Returns:
        Path: ログファイルのパス
    """
    if date is None:
        date = datetime.now()

    filename = date.strftime("%Y-%m-%d") + ".jsonl"
    return get_log_dir() / filename


def create_log_entry(
    active_app: str,
    window_title: str,
    ocr_text: str,
    ocr_confidence: float | None = None,
    timestamp: datetime | None = None
) -> LogEntry:
    """
    ログエントリを作成（初回作成時）

    Args:
        active_app: アクティブなアプリケーション名
        window_title: ウィンドウタイトル
        ocr_text: OCRで抽出されたテキスト
        ocr_confidence: OCR信頼度
        timestamp: タイムスタンプ。Noneの場合は現在時刻

    Returns:
        LogEntry: ログエントリ
    """
    if timestamp is None:
        timestamp = datetime.now()

    timestamp_str = timestamp.astimezone().isoformat()

    entry: LogEntry = {
        "start_time": timestamp_str,
        "end_time": timestamp_str,
        "duration_minutes": 1,
        "snapshot_count": 1,
        "active_app": active_app,
        "window_title": window_title,
        "ocr_text": ocr_text,
        "avg_ocr_confidence": ocr_confidence
    }

    return entry


def update_log_entry(
    entry: LogEntry,
    new_timestamp: datetime,
    new_confidence: float | None = None
) -> LogEntry:
    """
    既存のログエントリを更新（OCRテキストが同じ場合）

    Args:
        entry: 既存のログエントリ
        new_timestamp: 新しいタイムスタンプ
        new_confidence: 新しいOCR信頼度

    Returns:
        LogEntry: 更新されたログエントリ
    """
    from datetime import datetime as dt

    # start_timeからdatetimeオブジェクトを作成
    start_dt = dt.fromisoformat(entry["start_time"])

    # new_timestampがnaiveな場合はタイムゾーンを付与
    if new_timestamp.tzinfo is None:
        new_timestamp = new_timestamp.astimezone()

    # 経過時間を計算（分単位）
    duration = int((new_timestamp - start_dt).total_seconds() / 60) + 1

    # snapshot_countを増やす
    new_count = entry["snapshot_count"] + 1

    # 平均信頼度を再計算
    if new_confidence is not None and entry["avg_ocr_confidence"] is not None:
        old_total = entry["avg_ocr_confidence"] * entry["snapshot_count"]
        new_avg = (old_total + new_confidence) / new_count
    elif new_confidence is not None:
        new_avg = new_confidence
    else:
        new_avg = entry["avg_ocr_confidence"]

    # エントリを更新
    updated_entry: LogEntry = {
        "start_time": entry["start_time"],
        "end_time": new_timestamp.astimezone().isoformat(),
        "duration_minutes": duration,
        "snapshot_count": new_count,
        "active_app": entry["active_app"],
        "window_title": entry["window_title"],
        "ocr_text": entry["ocr_text"],
        "avg_ocr_confidence": new_avg
    }

    return updated_entry


def write_log_entry(entry: LogEntry) -> bool:
    """
    ログエントリをファイルに書き込む

    OCRテキストが空白の場合は保存をスキップする。

    Args:
        entry: ログエントリ

    Returns:
        bool: 書き込み成功した場合True、スキップした場合もTrue
    """
    # OCRテキストが空白の場合は保存しない
    ocr_text = entry.get("ocr_text", "")
    if not ocr_text or not ocr_text.strip():
        return True  # スキップしたが正常終了として扱う

    try:
        log_file = get_log_file_path()

        # JSON行を作成（ensure_ascii=Falseで日本語を保持）
        json_line = json.dumps(entry, ensure_ascii=False)

        # 追記モードで書き込み
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json_line + "\n")

        return True

    except Exception as e:
        print(f"Failed to write log entry: {e}")
        return False


def read_log_entries(date: datetime | None = None) -> list[LogEntry]:
    """
    ログエントリを読み込む

    Args:
        date: 対象日付。Noneの場合は今日

    Returns:
        list[LogEntry]: ログエントリのリスト
    """
    log_file = get_log_file_path(date)

    if not log_file.exists():
        return []

    entries = []
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
    except Exception as e:
        print(f"Failed to read log entries: {e}")

    return entries


def cleanup_old_logs(days: int = 30) -> int:
    """
    指定日数より古いログファイルを削除

    Args:
        days: 保持する日数。デフォルト30日

    Returns:
        int: 削除したファイル数
    """
    from datetime import timedelta

    log_dir = get_log_dir()
    cutoff_date = datetime.now() - timedelta(days=days)
    deleted_count = 0

    for log_file in log_dir.glob("*.jsonl"):
        try:
            # ファイル名から日付を取得（YYYY-MM-DD.jsonl）
            date_str = log_file.stem
            file_date = datetime.strptime(date_str, "%Y-%m-%d")

            if file_date < cutoff_date:
                log_file.unlink()
                print(f"Deleted old log: {log_file.name}")
                deleted_count += 1

        except ValueError:
            # ファイル名が日付形式でない場合はスキップ
            continue
        except Exception as e:
            print(f"Failed to delete {log_file}: {e}")

    return deleted_count
