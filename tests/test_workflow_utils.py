poet_Image_Description_Toolkit/test/test_workflow_utils.py
import unittest
import tempfile
import shutil
import os
from pathlib import Path
from poet_Image_Description_Toolkit.scripts.workflow_utils import (
    WorkflowConfig,
    WorkflowLogger,
    FileDiscovery,
    create_workflow_paths,
    get_script_compatibility_args,
    get_workflow_output_dir
)

class TestWorkflowConfig(unittest.TestCase):
    def setUp(self):
        # Create a temporary config file
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "workflow_config.json")
        self.config_content = {
            "workflow": {
                "base_output_dir": "workflow_output",
                "steps": {
                    "step1": {"enabled": True},
                    "step2": {"enabled": False}
                }
            },
            "file_patterns": {
                "images": ["*.jpg", "*.png"],
                "videos": ["*.mp4"]
            }
        }
        with open(self.config_path, "w") as f:
            import json
            json.dump(self.config_content, f)
        self.config = WorkflowConfig(self.config_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_load_config(self):
        self.assertEqual(self.config.config["workflow"]["base_output_dir"], "workflow_output")

    def test_get_default_config(self):
        default = self.config.get_default_config()
        self.assertIn("workflow", default)
        self.assertIn("steps", default["workflow"])

    def test_base_output_dir(self):
        self.assertEqual(str(self.config.base_output_dir), str(Path("workflow_output").resolve()))
        self.config.set_base_output_dir("custom_output")
        self.assertEqual(str(self.config.base_output_dir), str(Path("custom_output").resolve()))

    def test_is_step_enabled(self):
        self.assertTrue(self.config.is_step_enabled("step1"))
        self.assertFalse(self.config.is_step_enabled("step2"))
        self.assertTrue(self.config.is_step_enabled("nonexistent_step"))  # Defaults to True

    def test_get_step_config(self):
        self.assertEqual(self.config.get_step_config("step1"), {"enabled": True})
        self.assertEqual(self.config.get_step_config("step2"), {"enabled": False})
        self.assertEqual(self.config.get_step_config("nonexistent_step"), {})

    def test_get_file_patterns(self):
        self.assertEqual(self.config.get_file_patterns("images"), ["*.jpg", "*.png"])
        self.assertEqual(self.config.get_file_patterns("videos"), ["*.mp4"])
        self.assertEqual(self.config.get_file_patterns("docs"), [])

class TestWorkflowLogger(unittest.TestCase):
    def test_logger_methods(self):
        logger = WorkflowLogger(name="test_logger", log_level="DEBUG", log_to_file=False)
        # Just ensure these methods do not raise
        logger.info("info message")
        logger.warning("warning message")
        logger.error("error message")
        logger.debug("debug message")

class TestFileDiscovery(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "workflow_config.json")
        config_content = {
            "file_patterns": {
                "images": ["*.jpg", "*.png"],
                "videos": ["*.mp4"]
            }
        }
        with open(self.config_path, "w") as f:
            import json
            json.dump(config_content, f)
        self.config = WorkflowConfig(self.config_path)
        self.discovery = FileDiscovery(self.config)
        # Create some files
        Path(self.temp_dir, "a.jpg").touch()
        Path(self.temp_dir, "b.png").touch()
        Path(self.temp_dir, "c.mp4").touch()
        Path(self.temp_dir, "d.txt").touch()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_find_files_by_type(self):
        images = self.discovery.find_files_by_type(Path(self.temp_dir), "images")
        videos = self.discovery.find_files_by_type(Path(self.temp_dir), "videos")
        self.assertTrue(any(str(f).endswith(".jpg") for f in images))
        self.assertTrue(any(str(f).endswith(".png") for f in images))
        self.assertTrue(any(str(f).endswith(".mp4") for f in videos))
        self.assertFalse(any(str(f).endswith(".txt") for f in images + videos))

    def test_categorize_files(self):
        categories = self.discovery.categorize_files(Path(self.temp_dir))
        self.assertIn("images", categories)
        self.assertIn("videos", categories)
        self.assertTrue(any(str(f).endswith(".jpg") for f in categories["images"]))
        self.assertTrue(any(str(f).endswith(".mp4") for f in categories["videos"]))

    def test_get_relative_path_structure(self):
        base = Path(self.temp_dir)
        file_path = base / "subdir" / "file.jpg"
        rel = self.discovery.get_relative_path_structure(file_path, base)
        self.assertEqual(rel, Path("subdir/file.jpg"))

class TestUtilityFunctions(unittest.TestCase):
    def test_create_workflow_paths(self):
        base_dir = Path(tempfile.mkdtemp())
        paths = create_workflow_paths(base_dir)
        self.assertIsInstance(paths, dict)
        self.assertTrue(all(isinstance(p, Path) for p in paths.values()))
        shutil.rmtree(base_dir)

    def test_get_script_compatibility_args(self):
        config = WorkflowConfig()
        args = get_script_compatibility_args("ConvertImage.py", config, Path("input"), Path("output"))
        self.assertIsInstance(args, list)
        self.assertTrue(any("input" in str(a) or "output" in str(a) for a in args))

    def test_get_workflow_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        out_dir = get_workflow_output_dir("ConvertImage.py", fallback_dir=Path(temp_dir))
        self.assertTrue(isinstance(out_dir, Path) or out_dir is None)
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    unittest.main()
