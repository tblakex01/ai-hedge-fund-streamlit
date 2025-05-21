import importlib
import sys
import types
import unittest
from unittest import mock
from src.utils import llm as llm_module


# Provide dummy langchain modules required by agent imports
class FakeChatPromptTemplate:
    def __init__(self, *_, **__):
        pass

    @classmethod
    def from_messages(cls, *_):
        return cls()

    def invoke(self, *_):
        return "prompt"


sys.modules.setdefault(
    "langchain_core.prompts",
    types.SimpleNamespace(ChatPromptTemplate=FakeChatPromptTemplate),
)
sys.modules.setdefault(
    "langchain_core.messages",
    types.SimpleNamespace(HumanMessage=lambda *_, **__: object()),
)
sys.modules.setdefault("langchain_openai", types.SimpleNamespace(ChatOpenAI=object))

AGENT_FUNCS = [
    ("ben_graham", "generate_graham_output"),
    ("bill_ackman", "generate_ackman_output"),
    ("cathie_wood", "generate_cathie_wood_output"),
    ("charlie_munger", "generate_munger_output"),
    ("phil_fisher", "generate_fisher_output"),
    ("stanley_druckenmiller", "generate_druckenmiller_output"),
    ("warren_buffett", "generate_buffett_output"),
]


class TestAgentLLMParameters(unittest.TestCase):
    def test_agents_pass_model_to_call_llm(self):
        for mod_name, func_name in AGENT_FUNCS:
            with self.subTest(func=func_name):
                module = importlib.import_module(f"src.agents.{mod_name}")
                fake_result = object()
                with mock.patch(f"src.agents.{mod_name}.call_llm", return_value=fake_result) as mock_call:
                    result = getattr(module, func_name)(
                        ticker="T",
                        analysis_data={},
                        model_name="m",
                        model_provider="p",
                    )
                    self.assertIs(result, fake_result)
                    mock_call.assert_called_once()
                    kwargs = mock_call.call_args.kwargs
                    self.assertEqual(kwargs["model_name"], "m")
                    self.assertEqual(kwargs["model_provider"], "p")

    def test_agents_raise_without_model(self):
        fake_models_mod = types.SimpleNamespace(
            get_model_info=lambda name: types.SimpleNamespace(has_json_mode=lambda: True),
            get_model=lambda *_, **__: types.SimpleNamespace(
                with_structured_output=lambda *a, **k: types.SimpleNamespace(
                    invoke=lambda *_: object(),
                ),
            ),
        )
        for mod_name, func_name in AGENT_FUNCS:
            with self.subTest(func=func_name):
                module = importlib.import_module(f"src.agents.{mod_name}")
                with mock.patch.dict(sys.modules, {"src.llm.models": fake_models_mod}):
                    with mock.patch(
                        f"src.agents.{mod_name}.call_llm",
                        side_effect=llm_module.call_llm,
                    ):
                        with self.assertRaises(ValueError):
                            getattr(module, func_name)(
                                ticker="T",
                                analysis_data={},
                                model_name=None,
                                model_provider="p",
                            )
                        with self.assertRaises(ValueError):
                            getattr(module, func_name)(
                                ticker="T",
                                analysis_data={},
                                model_name="m",
                                model_provider=None,
                            )


if __name__ == "__main__":
    unittest.main()
