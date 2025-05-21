import importlib
import sys
import types
import unittest
from unittest import mock


class TestAgentProgress(unittest.TestCase):
    def setUp(self):
        fake_console = mock.MagicMock()
        fake_live_instance = mock.MagicMock()
        fake_live = mock.MagicMock(return_value=fake_live_instance)
        fake_table = mock.MagicMock()
        fake_style = types.SimpleNamespace()
        fake_text = mock.MagicMock()
        self.patcher = mock.patch.dict(
            sys.modules,
            {
                "rich.console": types.SimpleNamespace(Console=lambda: fake_console),
                "rich.live": types.SimpleNamespace(Live=fake_live),
                "rich.table": types.SimpleNamespace(Table=lambda **_: fake_table),
                "rich.style": types.SimpleNamespace(Style=lambda **_: fake_style),
                "rich.text": types.SimpleNamespace(Text=lambda: fake_text),
                "rich.control": types.SimpleNamespace(Control=lambda: object()),
                "rich.protocol": types.SimpleNamespace(RenderableType=object),
            },
        )
        self.patcher.start()
        sys.modules.pop("src.utils.progress", None)
        self.progress_mod = importlib.import_module("src.utils.progress")
        self.progress = self.progress_mod.AgentProgress()

    def tearDown(self):
        self.patcher.stop()
        if "src.utils.progress" in sys.modules:
            del sys.modules["src.utils.progress"]

    def test_update_and_reset_status(self):
        self.progress.update_status("agent_a", status="running")
        self.assertIn("agent_a", self.progress.agent_status)
        self.assertEqual(self.progress.agent_status["agent_a"]["status"], "running")
        self.progress.start()
        self.assertTrue(self.progress.started)
        self.progress.stop()
        self.assertFalse(self.progress.started)
