import unittest
from pathlib import Path
import tempfile
import os

# Import the target module and classes
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import descriptions_to_html

class TestSetupLogging(unittest.TestCase):
    def test_setup_logging(self):
        # Should not raise any exceptions
        try:
            descriptions_to_html.setup_logging(verbose=True)
        except Exception as e:
            self.fail(f"setup_logging raised an exception: {e}")

class TestDescriptionEntry(unittest.TestCase):
    def setUp(self):
        self.entry = descriptions_to_html.DescriptionEntry()
        self.entry.filename = "test.jpg"
        self.entry.filepath = "/images/test.jpg"
        self.entry.photo_date = "2024-06-01"
        self.entry.location = "Test Location"
        self.entry.camera = "Test Camera"
        self.entry.settings = "ISO 100, f/2.8"
        self.entry.model = "Test Model"
        self.entry.prompt_style = "detailed"
        self.entry.description = "A test description."
        self.entry.raw_metadata = {"meta": "data"}

    def test_to_html_basic(self):
        html = self.entry.to_html()
        self.assertIn("test.jpg", html)
        self.assertIn("A test description.", html)
        self.assertIn("Test Location", html)

    def test_to_html_with_details(self):
        html = self.entry.to_html(include_details=True)
        self.assertIn("ISO 100", html)
        self.assertIn("Test Camera", html)
        self.assertIn("meta", html)

class TestDescriptionsParser(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        self.temp_file.write(
            "Filename: test.jpg\n"
            "Filepath: /images/test.jpg\n"
            "Photo Date: 2024-06-01\n"
            "Location: Test Location\n"
            "Camera: Test Camera\n"
            "Settings: ISO 100, f/2.8\n"
            "Model: Test Model\n"
            "Prompt Style: detailed\n"
            "Description: A test description.\n"
            "---\n"
        )
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_parse(self):
        parser = descriptions_to_html.DescriptionsParser(Path(self.temp_file.name))
        entries = parser.parse()
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry.filename, "test.jpg")
        self.assertEqual(entry.description, "A test description.")

    def test_parse_empty(self):
        empty_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        empty_file.close()
        parser = descriptions_to_html.DescriptionsParser(Path(empty_file.name))
        entries = parser.parse()
        self.assertEqual(entries, [])
        os.unlink(empty_file.name)

class TestHTMLGenerator(unittest.TestCase):
    def setUp(self):
        entry = descriptions_to_html.DescriptionEntry()
        entry.filename = "test.jpg"
        entry.description = "A test description."
        self.entries = [entry]

    def test_generate(self):
        generator = descriptions_to_html.HTMLGenerator(self.entries, title="Test Title")
        html = generator.generate()
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Test Title", html)
        self.assertIn("test.jpg", html)
        self.assertIn("A test description.", html)

    def test_generate_toc(self):
        generator = descriptions_to_html.HTMLGenerator(self.entries)
        toc = generator._generate_toc()
        self.assertIn("test.jpg", toc)

    def test_generate_header(self):
        generator = descriptions_to_html.HTMLGenerator(self.entries)
        header = generator._generate_header()
        self.assertIn("<!DOCTYPE html>", header)
        self.assertIn("<head>", header)

class TestMainFunction(unittest.TestCase):
    def test_main_help(self):
        # Simulate running main with --help
        import subprocess
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/descriptions_to_html.py'))
        result = subprocess.run(['python3', script_path, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertIn(b'usage', result.stdout + result.stderr)

if __name__ == '__main__':
    unittest.main()
