poet_Image_Description_Toolkit/test/test_workflow.py
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import workflow

class TestWorkflowFunctions(unittest.TestCase):
    def test_sanitize_name_basic(self):
        self.assertEqual(workflow.sanitize_name("Test Model!@#"), "test_model")
        self.assertEqual(workflow.sanitize_name(""), "unknown")
        self.assertEqual(workflow.sanitize_name("Model__Name"), "model_name")
        self.assertEqual(workflow.sanitize_name("Model--Name"), "model--name")
        self.assertEqual(workflow.sanitize_name("Model.Name"), "model.name")

    @patch("workflow.WorkflowConfig")
    def test_get_effective_model_cmd_arg(self, MockConfig):
        args = MagicMock()
        args.model = "cmd_model"
        result = workflow.get_effective_model(args)
        self.assertEqual(result, "cmd_model")

    @patch("workflow.WorkflowConfig")
    def test_get_effective_model_config(self, MockConfig):
        args = MagicMock()
        args.model = None
        mock_config = MagicMock()
        mock_config.config = {
            "workflow": {
                "steps": {
                    "image_description": {
                        "model": "config_model"
                    }
                }
            }
        }
        MockConfig.return_value = mock_config
        result = workflow.get_effective_model(args)
        self.assertEqual(result, "config_model")

    @patch("workflow.WorkflowConfig")
    def test_get_effective_model_default(self, MockConfig):
        args = MagicMock()
        args.model = None
        mock_config = MagicMock()
        mock_config.config = {}
        MockConfig.return_value = mock_config
        result = workflow.get_effective_model(args)
        self.assertEqual(result, "unknown")

    @patch("workflow.WorkflowConfig")
    def test_get_effective_prompt_style_cmd_arg(self, MockConfig):
        args = MagicMock()
        args.prompt_style = "cmd_style"
        result = workflow.get_effective_prompt_style(args)
        self.assertEqual(result, "cmd_style")

    @patch("workflow.WorkflowConfig")
    def test_get_effective_prompt_style_config(self, MockConfig):
        args = MagicMock()
        args.prompt_style = None
        mock_config = MagicMock()
        mock_config.config = {
            "workflow": {
                "steps": {
                    "image_description": {
                        "prompt_style": "config_style"
                    }
                }
            }
        }
        MockConfig.return_value = mock_config
        result = workflow.get_effective_prompt_style(args)
        self.assertEqual(result, "config_style")

    @patch("workflow.WorkflowConfig")
    def test_get_effective_prompt_style_default(self, MockConfig):
        args = MagicMock()
        args.prompt_style = None
        mock_config = MagicMock()
        mock_config.config = {}
        MockConfig.return_value = mock_config
        result = workflow.get_effective_prompt_style(args)
        self.assertEqual(result, "unknown")

class TestWorkflowOrchestrator(unittest.TestCase):
    @patch("workflow.WorkflowConfig")
    def setUp(self, MockConfig):
        self.mock_config = MagicMock()
        MockConfig.return_value = self.mock_config
        self.orchestrator = workflow.WorkflowOrchestrator()

    @patch("workflow.WorkflowOrchestrator.extract_video_frames")
    def test_extract_video_frames(self, mock_extract):
        mock_extract.return_value = {"success": True, "frames": ["frame1.jpg", "frame2.jpg"]}
        result = self.orchestrator.extract_video_frames(Path("input"), Path("output"))
        self.assertTrue(result["success"])
        self.assertIn("frames", result)

    @patch("workflow.WorkflowOrchestrator.convert_images")
    def test_convert_images(self, mock_convert):
        mock_convert.return_value = {"success": True, "converted": ["img1.jpg", "img2.jpg"]}
        result = self.orchestrator.convert_images(Path("input"), Path("output"))
        self.assertTrue(result["success"])
        self.assertIn("converted", result)

    @patch("workflow.WorkflowOrchestrator.describe_images")
    def test_describe_images(self, mock_describe):
        mock_describe.return_value = {"success": True, "descriptions": ["desc1", "desc2"]}
        result = self.orchestrator.describe_images(Path("input"), Path("output"))
        self.assertTrue(result["success"])
        self.assertIn("descriptions", result)

    @patch("workflow.WorkflowOrchestrator.generate_html")
    def test_generate_html(self, mock_html):
        mock_html.return_value = {"success": True, "html_file": "report.html"}
        result = self.orchestrator.generate_html(Path("input"), Path("output"))
        self.assertTrue(result["success"])
        self.assertIn("html_file", result)

    @patch("workflow.WorkflowOrchestrator.run_workflow")
    def test_run_workflow(self, mock_run):
        mock_run.return_value = {"success": True, "workflow_results": {}}
        result = self.orchestrator.run_workflow(Path("input"), Path("output"), ["video", "convert", "describe", "html"])
        self.assertTrue(result["success"])
        self.assertIn("workflow_results", result)

    def test_update_statistics(self):
        self.orchestrator.statistics = {}
        self.orchestrator._update_statistics("step1", {"success": True, "processed": 5})
        self.assertIn("step1", self.orchestrator.statistics)
        self.assertEqual(self.orchestrator.statistics["step1"]["processed"], 5)

    def test_log_final_statistics(self):
        import datetime
        self.orchestrator.statistics = {"total_files_processed": 10}
        start = datetime.datetime.now()
        end = start + datetime.timedelta(seconds=5)
        # Should not raise
        self.orchestrator._log_final_statistics(start, end)

    def test_update_frame_extractor_config(self):
        # Should not raise
        self.orchestrator._update_frame_extractor_config("config.json", Path("output"))

if __name__ == "__main__":
    unittest.main()
