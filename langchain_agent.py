from typing import List, Tuple
from langchain import hub

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
from llm_models import LlmModels
from tools.json_load_tool import JSONLoadTool
from tools.general_conversation_tool import GeneralConversationTool

def _format_chat_history(chat_history: List[Tuple[str, str]]):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer

llm = LlmModels().get_default_chat_llm()

tools = [JSONLoadTool(), GeneralConversationTool()]
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)

