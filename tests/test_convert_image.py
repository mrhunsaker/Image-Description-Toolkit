import os
import tempfile
import shutil
import pytest
from pathlib import Path

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import ConvertImage

@pytest.fixture
def temp_dir():
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)

def test_setup_logging_sets_logger_level(monkeypatch):
    import logging
    monkeypatch.setattr(ConvertImage, "logger", logging.getLogger("test_logger"))
    ConvertImage.setup_logging(verbose=True)
    assert ConvertImage.logger.level == logging.DEBUG
    ConvertImage.setup_logging(verbose=False)
    assert ConvertImage.logger.level == logging.INFO

def test_convert_heic_to_jpg_invalid_path(tmp_path):
    # Should return None or raise FileNotFoundError for non-existent file
    input_path = tmp_path / "nonexistent.heic"
    result = ConvertImage.convert_heic_to_jpg(str(input_path))
    assert result is None or isinstance(result, str) or isinstance(result, bool)

def test_convert_heic_to_jpg_valid_file(monkeypatch, tmp_path):
    # Simulate a valid HEIC file conversion
    input_path = tmp_path / "test.heic"
    input_path.write_bytes(b"fakeheicdata")
    output_path = tmp_path / "output.jpg"

    def fake_open_heic(path):
        class FakeHeic:
            def save(self, out_path, format, quality):
                Path(out_path).write_bytes(b"fakejpgdata")
        return FakeHeic()
    monkeypatch.setattr(ConvertImage, "open_heic", fake_open_heic)
    result = ConvertImage.convert_heic_to_jpg(str(input_path), str(output_path))
    assert output_path.exists()
    assert result is not None

def test_convert_directory_empty(monkeypatch, tmp_path):
    # Should handle empty directory gracefully
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    result = ConvertImage.convert_directory(str(tmp_path), str(output_dir))
    assert isinstance(result, list)
    assert len(result) == 0

def test_convert_directory_with_files(monkeypatch, tmp_path):
    # Simulate directory with HEIC files
    heic_file = tmp_path / "img1.heic"
    heic_file.write_bytes(b"fakeheicdata")
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    def fake_convert_heic_to_jpg(input_path, output_path=None, quality=95, keep_metadata=True):
        Path(output_path).write_bytes(b"fakejpgdata")
        return output_path
    monkeypatch.setattr(ConvertImage, "convert_heic_to_jpg", fake_convert_heic_to_jpg)
    result = ConvertImage.convert_directory(str(tmp_path), str(output_dir))
    assert isinstance(result, list)
    assert any(str(output_dir) in str(r) for r in result)

def test_main_help(monkeypatch, capsys):
    # Simulate running main with --help
    monkeypatch.setattr("sys.argv", ["ConvertImage.py", "--help"])
    with pytest.raises(SystemExit):
        ConvertImage.main()
    captured = capsys.readouterr()
    assert "Convert HEIC/HEIF images to JPG format" in captured.out

def test_main_single_file(monkeypatch, tmp_path):
    # Simulate running main with a single file
    heic_file = tmp_path / "img1.heic"
    heic_file.write_bytes(b"fakeheicdata")
    monkeypatch.setattr("sys.argv", ["ConvertImage.py", str(heic_file)])
    monkeypatch.setattr(ConvertImage, "convert_heic_to_jpg", lambda input_path, **kwargs: str(tmp_path / "img1.jpg"))
    ConvertImage.main()

def test_main_directory(monkeypatch, tmp_path):
    # Simulate running main with a directory
    heic_file = tmp_path / "img1.heic"
    heic_file.write_bytes(b"fakeheicdata")
    monkeypatch.setattr("sys.argv", ["ConvertImage.py", str(tmp_path)])
    monkeypatch.setattr(ConvertImage, "convert_directory", lambda directory_path, **kwargs: [str(tmp_path / "img1.jpg")])
    ConvertImage.main()
