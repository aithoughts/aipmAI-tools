from typing import Any, Optional, Type

from embedchain.loaders.directory_loader import DirectoryLoader
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedDirectorySearchToolSchema(BaseModel):
    """DirectorySearchTool 的输入"""

    search_query: str = Field(
        ...,
        description="要用于搜索目录内容的必填搜索查询",
    )


class DirectorySearchToolSchema(FixedDirectorySearchToolSchema):
    """DirectorySearchTool 的输入"""

    directory: str = Field(..., description="要搜索的目录（必填）")


class DirectorySearchTool(RagTool):
    name: str = "搜索目录内容"
    description: str = (
        "用于对目录内容进行语义搜索查询的工具。"
    )
    args_schema: Type[BaseModel] = DirectorySearchToolSchema

    def __init__(self, directory: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if directory is not None:
            self.add(directory)
            self.description = f"用于对 {directory} 目录内容进行语义搜索查询的工具。"
            self.args_schema = FixedDirectorySearchToolSchema
            self._generate_description()

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs["loader"] = DirectoryLoader(config=dict(recursive=True))
        super().add(*args, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "directory" in kwargs:
            self.add(kwargs["directory"])

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
    