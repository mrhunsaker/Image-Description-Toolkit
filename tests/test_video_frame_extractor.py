import unittest
import os
import tempfile
import shutil
import numpy as np
from pathlib import Path
from scripts.video_frame_extractor import VideoFrameExtractor

class TestVideoFrameExtractor(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "test_config.json")
        self.extractor = VideoFrameExtractor(config_file=self.config_file, log_dir=self.test_dir)
        # Create dummy video file paths
        self.dummy_video_path = os.path.join(self.test_dir, "dummy.mp4")
        with open(self.dummy_video_path, "w") as f:
            f.write("dummy video content")

    def tearDown(self):
        # Remove temporary directory after test
        shutil.rmtree(self.test_dir)

    def test_supported_formats(self):
        formats = self.extractor.supported_formats
        self.assertIn('.mp4', formats)
        self.assertIn('.avi', formats)

    def test_load_config_and_get_default_config(self):
        config = self.extractor.get_default_config()
        self.assertIsInstance(config, dict)
        loaded_config = self.extractor.load_config(self.config_file)
        self.assertIsInstance(loaded_config, dict)

    def test_create_default_config_file(self):
        config = self.extractor.create_default_config_file(self.config_file)
        self.assertTrue(os.path.exists(self.config_file))
        self.assertIsInstance(config, dict)

    def test_calculate_scene_change(self):
        frame1 = np.zeros((10, 10, 3), dtype=np.uint8)
        frame2 = np.ones((10, 10, 3), dtype=np.uint8) * 255
        diff = self.extractor.calculate_scene_change(frame1, frame2)
        self.assertIsInstance(diff, float)
        self.assertGreaterEqual(diff, 0.0)

    def test_resize_frame(self):
        frame = np.ones((100, 200, 3), dtype=np.uint8) * 128
        resized = self.extractor.resize_frame(frame)
        self.assertIsInstance(resized, np.ndarray)
        self.assertEqual(resized.shape[2], 3)

    def test_find_video_files(self):
        # Should find the dummy video file
        found_files = self.extractor.find_video_files(self.test_dir)
        self.assertTrue(any(f.endswith('.mp4') for f in found_files))

    def test_log_final_summary(self):
        # Should not raise error
        self.extractor.statistics = {'start_time': 0, 'total_files': 1, 'total_frames': 10}
        try:
            self.extractor.log_final_summary()
        except Exception as e:
            self.fail(f"log_final_summary raised an exception: {e}")

    def test_run(self):
        # Should not raise error, even if no real video processing occurs
        try:
            self.extractor.run(self.test_dir)
        except Exception as e:
            self.fail(f"run raised an exception: {e}")

    def test_main_function_exists(self):
        # Just check that main exists and is callable
        from scripts.video_frame_extractor import main
        self.assertTrue(callable(main))

if __name__ == '__main__':
    unittest.main()
