import os
import json
import requests

from typing import Optional, Type, Any
from pydantic.v1 import BaseModel, Field
from crewai_tools.tools.base_tool import BaseTool

def _save_results_to_file(content: str) -> None:
    """将搜索结果保存到文件。"""
    filename = f"search_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(filename, 'w') as file:
        file.write(content)
    print(f"结果已保存到 {filename}")


class SerperDevToolSchema(BaseModel):
    """SerperDevTool 的输入。"""
    search_query: str = Field(..., description="要用于搜索互联网的必填搜索查询")

class SerperDevTool(BaseTool):
    name: str = "搜索互联网"
    description: str = "一个可以使用 search_query 搜索互联网的工具。"
    args_schema: Type[BaseModel] = SerperDevToolSchema
    search_url: str = "https://google.serper.dev/search"
    country: Optional[str] = None
    location: Optional[str] = None
    locale: Optional[str] = None
    n_results: int = Field(default=10, description="要返回的搜索结果数量")
    save_file: bool = Field(default=False, description="确定是否将结果保存到文件的标志")

    def _run(
        self,
        **kwargs: Any,
    ) -> Any:

        search_query = kwargs.get('search_query') or kwargs.get('query')
        save_file = kwargs.get('save_file', self.save_file)
        n_results = kwargs.get('n_results', self.n_results)

        payload = { "q": search_query, "num": n_results }
        payload["gl"] = self.country if self.country
        payload["location"] = self.country if self.location
        payload["hl"] = self.country if self.locale
        
        payload = json.dumps(payload)

        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", self.search_url, headers=headers, data=payload)
        results = response.json()
        if 'organic' in results:
            results = results['organic'][:self.n_results]
            string = []
            for result in results:
                try:
                    string.append('\n'.join([
                        f"标题：{result['title']}",
                        f"链接：{result['link']}",
                        f"片段：{result['snippet']}",
                        "---"
                    ]))
                except KeyError:
                    continue

            content = '\n'.join(string)
            if save_file:
                _save_results_to_file(content)
            return f"\n搜索结果：{content}\n"
        else:
            return results
