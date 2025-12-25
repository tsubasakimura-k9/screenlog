"""OCRモジュール - macOS Vision Frameworkを使用"""

from typing import NamedTuple


class OCRResult(NamedTuple):
    """OCR結果"""
    text: str
    confidence: float | None


def extract_text(image_path: str) -> OCRResult:
    """
    画像からテキストを抽出

    Args:
        image_path: 画像ファイルのパス

    Returns:
        OCRResult: 抽出されたテキストと信頼度
    """
    try:
        import Vision
        import Quartz
        from Foundation import NSURL

        # 画像を読み込む
        image_url = NSURL.fileURLWithPath_(image_path)
        image_source = Quartz.CGImageSourceCreateWithURL(image_url, None)

        if image_source is None:
            print(f"Failed to load image: {image_path}")
            return OCRResult(text="", confidence=None)

        cg_image = Quartz.CGImageSourceCreateImageAtIndex(image_source, 0, None)

        if cg_image is None:
            print(f"Failed to create CGImage: {image_path}")
            return OCRResult(text="", confidence=None)

        # Vision requestを作成
        request = Vision.VNRecognizeTextRequest.alloc().init()

        # 日本語と英語を認識
        request.setRecognitionLanguages_(["ja", "en"])

        # 認識精度を高精度に設定
        request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)

        # リクエストハンドラを作成して実行
        handler = Vision.VNImageRequestHandler.alloc().initWithCGImage_options_(
            cg_image, None
        )

        success = handler.performRequests_error_([request], None)

        if not success:
            print("OCR request failed")
            return OCRResult(text="", confidence=None)

        # 結果を取得
        results = request.results()

        if not results:
            return OCRResult(text="", confidence=None)

        # テキストと信頼度を集計
        texts = []
        total_confidence = 0.0
        count = 0

        for observation in results:
            if hasattr(observation, 'topCandidates_'):
                candidates = observation.topCandidates_(1)
                if candidates:
                    candidate = candidates[0]
                    texts.append(candidate.string())
                    total_confidence += candidate.confidence()
                    count += 1

        combined_text = "\n".join(texts)
        avg_confidence = total_confidence / count if count > 0 else None

        return OCRResult(text=combined_text, confidence=avg_confidence)

    except ImportError as e:
        print(f"Required framework not available: {e}")
        print("Please install: pip install pyobjc-framework-Vision pyobjc-framework-Quartz")
        return OCRResult(text="", confidence=None)
    except Exception as e:
        print(f"OCR error: {e}")
        return OCRResult(text="", confidence=None)
