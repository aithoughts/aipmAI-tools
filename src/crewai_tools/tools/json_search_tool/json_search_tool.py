from typing import Any, Optional, Type

from embedchain.models.data_type import DataType
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedJSONSearchToolSchema(BaseModel):
    """JSONSearchTool 的输入"""

    search_query: str = Field(
        ...,
        description="用来搜索JSON内容的搜索查询（必填）",
    )


class JSONSearchToolSchema(FixedJSONSearchToolSchema):
    """JSONSearchTool 的输入"""

    json_path: str = Field(..., description="想搜索的 json 路径（必填）")


class JSONSearchTool(RagTool):
    name: str = "搜索JSON内容"
    description: str = (
        "用来从JSON内容中语义搜索查询的工具。"
    )
    args_schema: Type[BaseModel] = JSONSearchToolSchema

    def __init__(self, json_path: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if json_path is not None:
            self.add(json_path)
            self.description = f"用来语义搜索 {json_path} JSON内容的查询工具。"
            self.args_schema = FixedJSONSearchToolSchema
            self._generate_description()

    def add(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        kwargs["data_type"] = DataType.JSON
        super().add(*args, **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "json_path" in kwargs:
            self.add(kwargs["json_path"])

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
