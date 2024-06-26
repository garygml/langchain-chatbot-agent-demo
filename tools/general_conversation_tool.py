from langchain.tools import Tool
import os
import json
from pathlib import Path
from langchain_core.documents import Document

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

response=("If this is a general greeting, return a final answer and do your greeting. "
          "If this is something that you cannot answer based on the context, "
          "return a final answer stating there is not enough information for you to answer that")

class GeneralConversationInput(BaseModel):
    query: Optional[str] = Field(description="user query")

class GeneralConversationTool(BaseTool):
    name = "GeneralTalk"
    description = ("useful for answering a generic question not related to customer ")
    args_schema: Type[BaseModel] = GeneralConversationInput

    def _run(
            self,
            account_number = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool"""
        return response


    async def _arun(
            self,
            account_number = None,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return response