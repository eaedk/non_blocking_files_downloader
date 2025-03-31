import os
import pytest
from src.downloader import get_response_with_ssl_fallback, download_and_log
from pathlib import Path

def test_ssl_fallback_success():
    url = "https://www.example.com/"
    response = get_response_with_ssl_fallback(url)
    assert response.status_code == 200

def test_download_creates_file(tmp_path: Path):
    test_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    output_path = tmp_path / "dummy.pdf"
    download_and_log(test_url, str(output_path))
    assert output_path.exists()
    assert output_path.stat().st_size > 0
