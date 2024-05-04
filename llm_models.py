import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI, OpenAI


from dotenv import load_dotenv
# Load .env file
load_dotenv()
google_api_key=os.getenv('GOOGLE_API_KEY')
openai_api_key=os.getenv('OPENAI_API_KEY')

class LlmModels:

    def get_default_llm(self):
        print("Using default model of:")
        return self.get_google_generative_ai_model()
    def get_default_chat_llm(self):
        print("Using default chat model of:")
        return self.get_chat_google_generative_ai_model()

    def get_chat_google_generative_ai_model(self):
        print("gemini-pro")
        llm = ChatGoogleGenerativeAI(model='gemini-pro',temperature=0, max_output_tokens=1024,top_p=0.8,top_k=2)
        return llm
    def get_google_generative_ai_model(self):
        print("gemini-pro")
        llm = GoogleGenerativeAI(model='gemini-pro',temperature=0, max_output_tokens=1024,top_p=0.8,top_k=2)
        return llm
    def get_ollama_llama3_model(self):
        print("llama3")
        llm = Ollama(model="llama3",temperature=0)
        return llm
    def get_ollama_llama2_model(self):
        print("llama2")
        llm = Ollama(model="llama2",temperature=0)
        return llm
    def get_ollama_mistral_model(self):
        print("mistral")
        llm = Ollama(model="mistral",temperature=0)
        return llm
    def get_chat_ollama_llama3_model(self):
        print("llama3")
        llm = ChatOllama(model="llama3",temperature=0)
        return llm
    def get_chat_ollama_llama2_model(self):
        print("llama2")
        llm = ChatOllama(model="llama2",temperature=0)
        return llm
    def get_chat_ollama_mistral_model(self):
        print("mistral")
        llm = ChatOllama(model="mistral",temperature=0)
        return llm
    def get_chat_openai_model(self):
        print("gpt-3.5-turbo-0125")
        llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
        return llm
    def get_openai_model(self):
        print("gpt-3.5-turbo-0125")
        llm = OpenAI(model="gpt-3.5-turbo-0125", temperature=0)
        return llm