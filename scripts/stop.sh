#!/bin/bash
# ScreenLog 停止スクリプト

PID_FILE="$HOME/ScreenLog/screenlog.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Stopping ScreenLog (PID: $PID)..."
        kill "$PID"
        rm "$PID_FILE"
        echo "ScreenLog stopped."
    else
        echo "ScreenLog is not running (stale PID file)."
        rm "$PID_FILE"
    fi
else
    echo "ScreenLog is not running."
fi
