from typing import Callable
from crewai_tools import BaseTool, tool

# def test_creating_a_tool_using_annotation():
# 	@tool("我的工具名称")
# 	def my_tool(question: str) -> str:
# 		"""清晰描述此工具的用途，您的代理需要此信息才能使用它。"""
# 		return question

# 	# 断言定义了所有正确的属性
# 	assert my_tool.name == "我的工具名称"
# 	assert my_tool.description == "我的工具名称(question: 'string') - 清晰描述此工具的用途，您的代理需要此信息才能使用它。"
# 	assert my_tool.args_schema.schema()["properties"] == {'question': {'title': '问题', 'type': 'string'}}
# 	assert my_tool.func("生命的意义是什么？") == "生命的意义是什么？"

# 	# 断言 langchain 工具转换按预期工作
# 	converted_tool = my_tool.to_langchain()
# 	assert converted_tool.name == "我的工具名称"
# 	assert converted_tool.description == "我的工具名称(question: 'string') - 清晰描述此工具的用途，您的代理需要此信息才能使用它。"
# 	assert converted_tool.args_schema.schema()["properties"] == {'question': {'title': '问题', 'type': 'string'}}
# 	assert converted_tool.func("生命的意义是什么？") == "生命的意义是什么？"

# def test_creating_a_tool_using_baseclass():
# 	class MyCustomTool(BaseTool):
# 		name: str = "我的工具名称"
# 		description: str = "清晰描述此工具的用途，您的代理需要此信息才能使用它。"

# 		def _run(self, question: str) -> str:
# 			return question

# 	my_tool = MyCustomTool()
# 	# 断言定义了所有正确的属性
# 	assert my_tool.name == "我的工具名称"
# 	assert my_tool.description == "我的工具名称(question: 'string') - 清晰描述此工具的用途，您的代理需要此信息才能使用它。"
# 	assert my_tool.args_schema.schema()["properties"] == {'question': {'title': '问题', 'type': 'string'}}
# 	assert my_tool.run("生命的意义是什么？") == "生命的意义是什么？"

# 	# 断言 langchain 工具转换按预期工作
# 	converted_tool = my_tool.to_langchain()
# 	assert converted_tool.name == "我的工具名称"
# 	assert converted_tool.description == "我的工具名称(question: 'string') - 清晰描述此工具的用途，您的代理需要此信息才能使用它。"
# 	assert converted_tool.args_schema.schema()["properties"] == {'question': {'title': '问题', 'type': 'string'}}
# 	assert converted_tool.run("生命的意义是什么？") == "生命的意义是什么？"

def test_setting_cache_function():
	class MyCustomTool(BaseTool):
		name: str = "我的工具名称"
		description: str = "清晰描述此工具的用途，您的代理需要此信息才能使用它。"
		cache_function: Callable = lambda: False

		def _run(self, question: str) -> str:
			return question

	my_tool = MyCustomTool()
	# 断言定义了所有正确的属性
	assert my_tool.cache_function() == False

# def test_default_cache_function_is_true():
# 	class MyCustomTool(BaseTool):
# 		name: str = "我的工具名称"
# 		description: str = "清晰描述此工具的用途，您的代理需要此信息才能使用它。"

# 		def _run(self, question: str) -> str:
# 			return question

# 	my_tool = MyCustomTool()
# 	# 断言定义了所有正确的属性
# 	assert my_tool.cache_function() == True