# src/ai/tools/lc_tools.py
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools import DuckDuckGoSearchResults, WikipediaQueryRun
from langchain_community.utilities import (
    WikipediaAPIWrapper,
    DuckDuckGoSearchAPIWrapper,
)
from pydantic_ai.ext.langchain import LangChainToolset

lc_fm_toolset = LangChainToolset(tools=FileManagementToolkit().get_tools(), id="FileManagementToolkit")
wiki_api_wrapper = WikipediaAPIWrapper(
    top_k_results=1, lang="ru", doc_content_chars_max=1000
)
duckduckgo_wrapper = DuckDuckGoSearchAPIWrapper(region="ru-ru")
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)
duckduckgo_tool = DuckDuckGoSearchResults(api_wrapper=duckduckgo_wrapper)

search_toolset = LangChainToolset(tools=[wiki_tool, duckduckgo_tool], id="SearchToolset")