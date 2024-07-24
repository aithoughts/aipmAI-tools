from typing import Any, List, Optional, Type

from embedchain.loaders.github import GithubLoader
from pydantic.v1 import BaseModel, Field

from ..rag.rag_tool import RagTool


class FixedGithubSearchToolSchema(BaseModel):
    """GithubSearchTool 的输入"""

    search_query: str = Field(
        ...,
        description="用来搜索 github 仓库内容的搜索查询（必填）",
    )


class GithubSearchToolSchema(FixedGithubSearchToolSchema):
    """GithubSearchTool 的输入"""

    github_repo: str = Field(..., description="想搜索的 github 仓库（必填）")
    content_types: List[str] = Field(
        ...,
        description="包含在搜索中的必填内容类型，选项：[code, repo, pr, issue]",
    )


class GithubSearchTool(RagTool):
    name: str = "搜索 github 仓库内容"
    description: str = "用来从 github 仓库内容中语义搜索查询的工具。这不是 GitHub API，而是提供语义搜索功能的工具。"
    summarize: bool = False
    gh_token: str
    args_schema: Type[BaseModel] = GithubSearchToolSchema
    content_types: List[str]

    def __init__(self, github_repo: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if github_repo is not None:
            self.add(repo=github_repo)
            self.description = f"用来语义搜索 {github_repo} github 仓库内容的查询工具。这不是 GitHub API，而是提供语义搜索功能的工具。"
            self.args_schema = FixedGithubSearchToolSchema
            self._generate_description()

    def add(
        self,
        repo: str,
        content_types: List[str] | None = None,
        **kwargs: Any,
    ) -> None:
        content_types = content_types or self.content_types

        kwargs["data_type"] = "github"
        kwargs["loader"] = GithubLoader(config={"token": self.gh_token})
        super().add(f"repo:{repo} type:{','.join(content_types)}", **kwargs)

    def _before_run(
        self,
        query: str,
        **kwargs: Any,
    ) -> Any:
        if "github_repo" in kwargs:
            self.add(
                repo=kwargs["github_repo"], content_types=kwargs.get("content_types")
            )

    def _run(
        self,
        search_query: str,
        **kwargs: Any,
    ) -> Any:
        return super()._run(query=search_query, **kwargs)
