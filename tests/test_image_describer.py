import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import base64
import os

# Import the module and class to test
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from image_describer import ImageDescriber, setup_logging, get_default_prompt_style, get_available_prompt_styles

class TestImageDescriber(unittest.TestCase):
    def setUp(self):
        self.config_file = "image_describer_config.json"
        self.image_path = Path("test_image.jpg")
        self.describer = ImageDescriber(config_file=self.config_file)

    @patch("image_describer.logging")
    def test_setup_logging(self, mock_logging):
        setup_logging(log_dir="logs", verbose=True)
        mock_logging.basicConfig.assert_called()

    def test_get_default_config(self):
        config = self.describer.get_default_config()
        self.assertIsInstance(config, dict)
        self.assertIn("model", config)
        self.assertIn("prompt_styles", config)

    def test_get_prompt(self):
        prompt = self.describer.get_prompt()
        self.assertIsInstance(prompt, str)
        self.assertTrue(len(prompt) > 0)

    def test_get_model_settings(self):
        settings = self.describer.get_model_settings()
        self.assertIsInstance(settings, dict)
        self.assertIn("max_image_size", settings)

    def test_is_supported_image(self):
        supported = self.describer.is_supported_image(Path("photo.jpg"))
        unsupported = self.describer.is_supported_image(Path("document.pdf"))
        self.assertTrue(supported)
        self.assertFalse(unsupported)

    @patch("image_describer.ImageDescriber.optimize_image")
    def test_encode_image_to_base64(self, mock_optimize):
        mock_optimize.return_value = b"fakeimagebytes"
        result = self.describer.encode_image_to_base64(self.image_path)
        self.assertIsInstance(result, str)
        self.assertEqual(result, base64.b64encode(b"fakeimagebytes").decode())

    @patch("image_describer.ImageDescriber.encode_image_to_base64")
    @patch("image_describer.ImageDescriber.get_prompt")
    def test_get_image_description(self, mock_get_prompt, mock_encode):
        mock_get_prompt.return_value = "Describe this image."
        mock_encode.return_value = base64.b64encode(b"img").decode()
        # Simulate API call
        with patch("image_describer.ImageDescriber._call_ollama_api", return_value="A beautiful sunset."):
            desc = self.describer.get_image_description(self.image_path)
            self.assertIsInstance(desc, str)
            self.assertIn("sunset", desc)

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_write_description_to_file(self, mock_open):
        result = self.describer.write_description_to_file(
            self.image_path, "A description", Path("output.txt")
        )
        self.assertTrue(result)
        mock_open.assert_called_with("output.txt", "w", encoding="utf-8")

    @patch("image_describer.ImageDescriber.is_supported_image")
    @patch("image_describer.ImageDescriber.get_image_description")
    @patch("image_describer.ImageDescriber.write_description_to_file")
    def test_process_directory(self, mock_write, mock_get_desc, mock_is_supported):
        mock_is_supported.return_value = True
        mock_get_desc.return_value = "desc"
        mock_write.return_value = True
        test_dir = Path("test_images")
        os.makedirs(test_dir, exist_ok=True)
        with open(test_dir / "img1.jpg", "w") as f:
            f.write("fake")
        self.describer.process_directory(test_dir)
        mock_write.assert_called()

    @patch("image_describer.ImageDescriber.extract_metadata")
    def test_extract_metadata(self, mock_extract):
        mock_extract.return_value = {"DateTime": "2023:01:01 12:00:00"}
        metadata = self.describer.extract_metadata(self.image_path)
        self.assertIn("DateTime", metadata)

    def test_format_metadata(self):
        metadata = {"DateTime": "2023:01:01 12:00:00", "Camera": "Canon"}
        formatted = self.describer.format_metadata(metadata)
        self.assertIsInstance(formatted, str)
        self.assertIn("Canon", formatted)

class TestPromptStyles(unittest.TestCase):
    @patch("image_describer.open", new_callable=unittest.mock.mock_open, read_data='{"prompt_styles": {"detailed": "Describe"}}')
    def test_get_default_prompt_style(self, mock_open):
        style = get_default_prompt_style("image_describer_config.json")
        self.assertIsInstance(style, str)

    @patch("image_describer.open", new_callable=unittest.mock.mock_open, read_data='{"prompt_styles": {"detailed": "Describe", "brief": "Summarize"}}')
    def test_get_available_prompt_styles(self, mock_open):
        styles = get_available_prompt_styles("image_describer_config.json")
        self.assertIsInstance(styles, list)
        self.assertIn("detailed", styles)

if __name__ == "__main__":
    unittest.main()
