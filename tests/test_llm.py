import sys
import types
import unittest
from typing import Literal
from unittest import mock

# Provide dummy modules for rich which is required by progress
sys.modules.setdefault("rich.console", mock.MagicMock())
sys.modules.setdefault("rich.live", mock.MagicMock())
sys.modules.setdefault("rich.table", mock.MagicMock())
sys.modules.setdefault("rich.style", mock.MagicMock())
sys.modules.setdefault("rich.text", mock.MagicMock())

from src.utils.llm import create_default_response, extract_json_from_deepseek_response


class DummyModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

DummyModel.model_fields = {
    'name': types.SimpleNamespace(annotation=str),
    'value': types.SimpleNamespace(annotation=float),
    'count': types.SimpleNamespace(annotation=int),
    'data': types.SimpleNamespace(annotation=dict),
    'label': types.SimpleNamespace(annotation=Literal['A', 'B'])
}


class TestLLMUtils(unittest.TestCase):
    def test_create_default_response(self):
        result = create_default_response(DummyModel)
        self.assertEqual(result.name, "Error in analysis, using default")
        self.assertEqual(result.value, 0.0)
        self.assertEqual(result.count, 0)
        self.assertIsNone(result.data)
        self.assertEqual(result.label, 'A')

    def test_extract_json_success(self):
        content = "prefix```json\n{\"a\": 1}\n```suffix"
        self.assertEqual(extract_json_from_deepseek_response(content), {"a": 1})

    def test_extract_json_failure(self):
        self.assertIsNone(extract_json_from_deepseek_response("no json here"))

    def test_extract_json_malformed_json(self):
        content = "prefix```json\n{\"a\": 1\n```suffix"  # missing closing brace
        self.assertIsNone(extract_json_from_deepseek_response(content))

    def test_extract_json_bad_markdown(self):
        content = "prefix```js\n{\"a\": 1}\n```suffix"  # wrong code block tag
        self.assertIsNone(extract_json_from_deepseek_response(content))


if __name__ == "__main__":
    unittest.main()
