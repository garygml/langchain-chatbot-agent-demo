from typing import Optional, Type
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain.tools import Tool
import os
import json
from pathlib import Path
from langchain_core.documents import Document

def load_json(account_number: Optional[str]) -> str:
    extensions = [".json"]
    file_paths = []
    for root, dirs, files in os.walk("../json"):
        for file in files:
            _, file_extension = os.path.splitext(file)
            if file_extension.lower() in extensions:
                file_paths.append(os.path.join(root, file))
    print(file_paths)

    data_list = []
    for file_path in file_paths:
        data = json.loads(Path(file_path).read_text())
        data_list.append(data)
    if len(data_list) == 0:
        return ("No data was found for this customer, return a final answer that you are not able to find "
                "this information")
    response = (json.dumps(data_list))
    return response

def summarize(question: str) -> str:
    llm = ChatOllama(model="llama2")
    docs = load_json("1111")
    new_docs = []
    for i in range(len(docs)):
        doc = Document(page_content=json.dumps(docs[i]), metadata={'source': 'langchain'})
        new_docs.append(doc)

    system_template = """

        You are part of a process to summarize what was in the documents, 
        and try to identify the answer based on the question

        Documents:
        {context}

    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    # agent = create_react_agent(self.llm, self.tools, prompt)
    document_chain = create_stuff_documents_chain(llm, prompt)

    # agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    # agent_executor.invoke({
    #     "context": new_docs,
    #     "input": "and what day was that?",
    #     "chat_history": [
    #         HumanMessage(content="How much did i pay pre-tip for the burger place i went to in 2019"),
    #         AIMessage(
    #             content="Hello there! I'm happy to help you with your query. Based on the document we found, it appears that you purchased a meal at Nobel Burger located in YYZ Terminal 3. According to the receipt, you paid a total of $18.34 for your meal, which includes a subtotal of $15.82 and a tip of $2.52.\nI hope this information helps you! Let me know if you have any other questions.")
    #         #HumanMessage(content="and what day was that?")
    #         # AIMessage(content="Of course! According to the receipt, the purchase was made on April 14th, 2019 at 4:44 PM."),
    #         # HumanMessage(content="was I paying with a card for that meal?")
    #     ],
    # })
    answer = document_chain.invoke(
        {
            "context": new_docs,
            "messages": [
                HumanMessage(content=question)
            ],
        }
    )
    # print(answer)
    return answer


class DocumentSummaryInput(BaseModel):
    question: str = Field(description="the full question in plain string related to what you want to find")
    # docs: str = Field(description="documents in plain string format")


class DocumentSummaryTool(BaseTool):
    name = "CustomerReceiptSummary"
    description = ("use this tool when handling customer receipts, "
                   "the tool provides a summary of the receipt documents based on the question")
    args_schema: Type[BaseModel] = DocumentSummaryInput

    def _run(
        self,
        question: str,
        # docs: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return summarize(question)

    async def _arun(
        self,
        question: str,
        # docs: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return summarize(question)