from typing import List, Tuple
from langchain import hub

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
from llm_models import LlmModels
from tools.get_receipt_tool import GetReceiptTool
from tools.general_conversation_tool import GeneralConversationTool
from langchain_core.prompts import ChatPromptTemplate

def _format_chat_history(chat_history: List[Tuple[str, str]]):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer

llm = LlmModels().get_default_chat_llm()

tools = [GetReceiptTool(), GeneralConversationTool()]
#prompt = hub.pull("hwchase17/react")

template = """
You are a online chatbot, your customer asked a question and you are trying to answer that. 
You have access to the following tools if needed to help you:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question 

Begin!

Previous conversation history: {chat_history}

Question: {input}

Thought: {agent_scratchpad}

"""

prompt = ChatPromptTemplate.from_template(template)

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)

