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


DummyModel.model_fields = {"name": types.SimpleNamespace(annotation=str), "value": types.SimpleNamespace(annotation=float), "count": types.SimpleNamespace(annotation=int), "data": types.SimpleNamespace(annotation=dict), "label": types.SimpleNamespace(annotation=Literal["A", "B"])}


class TestLLMUtils(unittest.TestCase):
    def test_create_default_response(self):
        result = create_default_response(DummyModel)
        self.assertEqual(result.name, "Error in analysis, using default")
        self.assertEqual(result.value, 0.0)
        self.assertEqual(result.count, 0)
        self.assertIsNone(result.data)
        self.assertEqual(result.label, "A")

    def test_extract_json_success(self):
        content = 'prefix```json\n{"a": 1}\n```suffix'
        self.assertEqual(extract_json_from_deepseek_response(content), {"a": 1})

    def test_extract_json_failure(self):
        self.assertIsNone(extract_json_from_deepseek_response("no json here"))

    def test_extract_json_with_script(self):
        content = 'prefix```json\n{"a": "<script>1</script>"}\n```suffix'
        result = extract_json_from_deepseek_response(content)
        self.assertEqual(result, {"a": "<script>1</script>"})

    def test_call_llm_default_factory(self):
        from src.utils import llm as llm_module

        class FakeLLM:
            def with_structured_output(self, *_, **__):
                return self

            def invoke(self, *_):
                raise RuntimeError("boom")

        fake_models_mod = types.SimpleNamespace(
            get_model_info=lambda name: types.SimpleNamespace(has_json_mode=lambda: True),
            get_model=lambda *args, **kwargs: FakeLLM(),
        )
        with mock.patch.dict(sys.modules, {"src.llm.models": fake_models_mod}), mock.patch.object(llm_module.progress, "update_status"):
            factory_called = {}

            def factory():
                factory_called["called"] = True
                return DummyModel(name="d", value=1.0, count=1, data={}, label="A")

            result = llm_module.call_llm("prompt", "model", "provider", DummyModel, default_factory=factory)

        self.assertTrue(factory_called.get("called"))
        self.assertEqual(result.name, "d")


if __name__ == "__main__":
    unittest.main()
