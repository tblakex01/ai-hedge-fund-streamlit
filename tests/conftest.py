import sys
import types


class FakeChatPromptTemplate:
    @classmethod
    def from_messages(cls, *_, **__):
        return cls()

    def invoke(self, *_):
        return "prompt"


sys.modules.setdefault(
    "langchain_core.prompts",
    types.SimpleNamespace(ChatPromptTemplate=FakeChatPromptTemplate),
)
sys.modules.setdefault(
    "langchain_core.messages",
    types.SimpleNamespace(
        HumanMessage=lambda *_, **__: object(),
        BaseMessage=object,
        BaseMessageChunk=object,
    ),
)
sys.modules.setdefault("langchain_openai", types.SimpleNamespace(ChatOpenAI=object))
