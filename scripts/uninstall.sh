#!/bin/bash
# ScreenLog アンインストールスクリプト

PLIST_NAME="com.screenlog.agent.plist"
PLIST_DST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "=== ScreenLog Uninstaller ==="
echo ""

# エージェントを停止
if [ -f "$PLIST_DST" ]; then
    echo "Stopping ScreenLog agent..."
    launchctl unload "$PLIST_DST" 2>/dev/null || true
    rm "$PLIST_DST"
    echo "Agent removed."
else
    echo "Agent not installed."
fi

echo ""
echo "=== Uninstallation Complete ==="
echo ""
echo "Note: Log files are preserved at $HOME/ScreenLog/"
echo "To delete logs: rm -rf $HOME/ScreenLog"
