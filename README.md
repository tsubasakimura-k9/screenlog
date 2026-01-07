# ScreenLog

macOS上で動作する作業ログ自動生成ツール。スクリーンショットを定期的に取得し、ローカルOCRでテキスト化して保存する。

## 特徴

- **完全ローカル処理**: スクリーンショット・OCR処理はすべてローカルで完結（外部APIを使わない）
- **自動記録**: 1分間隔でバックグラウンド動作
- **日本語・英語対応**: macOS Vision Frameworkによる高精度OCR
- **AI連携前提**: 蓄積されたログをAIに渡して作業時間をまとめられる

## 必要条件

- macOS 12.0以降
- Python 3.10以降
- 画面収録権限（Screen Recording）
- アクセシビリティ権限（Accessibility）

## インストール

```bash
# リポジトリをクローン
cd /path/to/screenlog

# 仮想環境を作成（推奨）
python3 -m venv venv
source venv/bin/activate

# 依存ライブラリをインストール
pip install -r requirements.txt
```

## 使い方

### 起動

```bash
# 起動スクリプトを使用
./scripts/start.sh

# または直接実行
python -m screenlog.main

# キャプチャ間隔を指定（秒）
python -m screenlog.main -i 30

# 1回だけキャプチャして終了
python -m screenlog.main --once
```

### 停止

`Ctrl+C` で停止。

### ログの確認

ログは `~/Library/Application Support/ScreenLog/logs/` に日付別のJSONLファイルとして保存される。

```bash
# 今日のログを確認
cat ~/Library/Application\ Support/ScreenLog/logs/$(date +%Y-%m-%d).jsonl

# 整形して表示
cat ~/Library/Application\ Support/ScreenLog/logs/$(date +%Y-%m-%d).jsonl | jq .
```

## ログ形式

各エントリはJSON形式で1行ずつ保存される。

```json
{
  "timestamp": "2024-12-23T14:35:00+09:00",
  "active_app": "Visual Studio Code",
  "window_title": "main.py - MyProject",
  "ocr_text": "def process_screenshot():\n    # スクリーンショットを処理する...",
  "ocr_confidence": 0.85
}
```

## AIによる作業まとめ

ログファイルをAI（Claude等）に渡して、以下のようなプロンプトで要約させる：

```
以下は今日の作業ログです。JSONLファイルの各行がスクリーンショットから取得した情報です。
これを読み取って、何時から何時に何をしていたかを時系列でまとめてください。
細かいエントリは適宜集約し、作業の切り替わりがわかるようにしてください。

---
[JSONLファイルの内容をここに貼り付け]
```

## 権限設定

初回実行時に以下の権限を求められる：

1. **画面収録（Screen Recording）**
   - システム設定 > プライバシーとセキュリティ > 画面収録
   - ターミナル（または使用するアプリ）を許可

2. **アクセシビリティ（Accessibility）**
   - システム設定 > プライバシーとセキュリティ > アクセシビリティ
   - ターミナル（または使用するアプリ）を許可

## ファイル構成

```
~/Library/Application Support/ScreenLog/
├── logs/
│   ├── 2024-12-21.jsonl
│   ├── 2024-12-22.jsonl
│   └── 2024-12-23.jsonl
└── tmp/                      # 一時ファイル（自動削除）
```

## ライセンス

MIT License
