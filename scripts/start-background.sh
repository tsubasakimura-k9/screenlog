#!/bin/bash
# ScreenLog バックグラウンド起動スクリプト
# ターミナルの画面収録権限を利用して実行
#
# Usage:
#   ./start-background.sh              # デフォルト設定で起動
#   ./start-background.sh --interval 60  # 60秒間隔で起動

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PID_FILE="$HOME/ScreenLog/screenlog.pid"
LOG_FILE="$HOME/ScreenLog/screenlog.log"

cd "$PROJECT_DIR"

# 既に実行中か確認
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "ScreenLog is already running (PID: $OLD_PID)"
        exit 1
    fi
fi

# ログディレクトリ作成
mkdir -p "$HOME/ScreenLog/logs"

# 仮想環境をアクティベートして実行
source venv/bin/activate

echo "Starting ScreenLog in background..."
nohup python -m screenlog.main "$@" > "$LOG_FILE" 2>&1 &
PID=$!
echo $PID > "$PID_FILE"

echo "ScreenLog started (PID: $PID)"
echo "Log file: $LOG_FILE"
echo ""
echo "Commands:"
echo "  Stop:   $SCRIPT_DIR/stop.sh"
echo "  Logs:   tail -f $LOG_FILE"
