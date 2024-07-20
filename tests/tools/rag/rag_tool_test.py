import os
from tempfile import NamedTemporaryFile
from typing import cast
from unittest import mock

from pytest import fixture

# from langchain_ollama.llms import OllamaLLM
# from langchain_ollama import OllamaEmbeddings

# model = OllamaLLM(model="llama3")
# embeddings = OllamaEmbeddings(model="llama3")

from crewai_tools.adapters.embedchain_adapter import EmbedchainAdapter
from crewai_tools.tools.rag.rag_tool import RagTool


@fixture(autouse=True)
def mock_embedchain_db_uri():
    with NamedTemporaryFile() as tmp:
        uri = f"sqlite:///{tmp.name}"
        with mock.patch.dict(os.environ, {"EMBEDCHAIN_DB_URI": uri}):
            yield


def test_custom_llm_and_embedder():
    class MyTool(RagTool):
        pass

    tool = MyTool(
        config=dict(
            llm=dict(
                provider="ollama",
                config=dict(model="llama3:latest"),
            ),
            embedder=dict(
                provider="ollama",
                config=dict(model="llama3:latest"),
            ),
        )
    )
    assert tool.adapter is not None
    assert isinstance(tool.adapter, EmbedchainAdapter)

    adapter = cast(EmbedchainAdapter, tool.adapter)
    assert adapter.embedchain_app.llm.config.model == "llama3:latest"
    assert (
        adapter.embedchain_app.embedding_model.config.model == "llama3:latest"
    )
