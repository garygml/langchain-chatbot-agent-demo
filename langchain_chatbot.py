from langchain_community.llms import Ollama
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
import os
import json
from pathlib import Path
from langchain_core.documents import Document
from llm_models import LlmModels

class MyLangChainChatBot:
    def __init__(self):
        # Load the Llama2 model
        self.llm = LlmModels.get_default_llm()
        #receipt_search_tool = ReceiptSearchTool()
        self.tools = []

    def run(self):
        system_template = """

            You are a online chatbot. Your customer asked you a question and in the system some of his documents are found. 

            Answer the question to the customer based on the content in the documents found. 

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
        document_chain = create_stuff_documents_chain(self.llm, prompt)

        docs = self.load_json()
        new_docs = []
        for i in range(len(docs)):
            doc = Document(page_content=json.dumps(docs[i]), metadata={'source': 'langchain'})
            new_docs.append(doc)

        print(new_docs)

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
                    HumanMessage(content="How much did i pay pre-tip for the burger place i went to in 2019"),
                    AIMessage(
                        content="Hello there! I'm happy to help you with your query. Based on the document we found, it appears that you purchased a meal at Nobel Burger located in YYZ Terminal 3. According to the receipt, you paid a total of $18.34 for your meal, which includes a subtotal of $15.82 and a tip of $2.52.\nI hope this information helps you! Let me know if you have any other questions."),
                    HumanMessage(content="and what day was that?")
                    # AIMessage(content="Of course! According to the receipt, the purchase was made on April 14th, 2019 at 4:44 PM."),
                    # HumanMessage(content="was I paying with a card for that meal?")
                ],
            }
        )
        print(answer)
        return answer

    def load_json(self):
        extensions = [".json"]
        file_paths = []
        for root, dirs, files in os.walk("json"):
            for file in files:
                _, file_extension = os.path.splitext(file)
                if file_extension.lower() in extensions:
                    file_paths.append(os.path.join(root, file))
        print(file_paths)

        data_list = []
        for file_path in file_paths:
            # loader = JSONLoader(
            #    file_path = file_path
            # )
            # data = loader.load()
            data = json.loads(Path(file_path).read_text())
            data_list.append(data)
        return data_list
