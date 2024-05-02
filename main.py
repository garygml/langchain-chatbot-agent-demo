from fastapi import FastAPI
from langchain_chatbot import MyLangChainChatBot
from langchain_agent import agent_executor
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/testChatBot")
async def testMyLangChainChatBot():
    chatbot = MyLangChainChatBot()
    return chatbot.run()

@app.get("/testAgent")
async def testAgentExecutor():
    original_query = "I had a receipt for a burger place in 2019, do you know how much I paid for tips?"
    followup_query = "and what day was that for?"
    smalltalk = "How are you today?"
    chat_history = [
        (
            "I had a receipt for a burger place in 2019, do you know how much I paid?",
            "Hello there! I'm happy to help you with your query. Based on the document we found, it appears that you purchased a meal at Nobel Burger located in YYZ Terminal 3. According to the receipt, you paid a total of $18.34 for your meal, which includes a subtotal of $15.82 and a tip of $2.52.\nI hope this information helps you! Let me know if you have any other questions.",
        )
    ]
    print(agent_executor.invoke({"input": original_query}))  # noqa: T201
    print(agent_executor.invoke({"input": smalltalk}))
    print(  # noqa: T201
        agent_executor.invoke({"input": followup_query, "chat_history": chat_history})
    )
    return []

class AnswerInput(BaseModel):
    input: str
    chat_history: list

@app.post("/answer")
async def agentExecutorAnswer(answer_input: AnswerInput):
    input = answer_input.input
    chat_history = answer_input.chat_history
    answer = agent_executor.invoke({"input": input, "chat_history": chat_history})
    print(answer)
    return answer