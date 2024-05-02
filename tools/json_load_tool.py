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

def load_json(account_number: Optional[str]) -> str:
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
        data = json.loads(Path(file_path).read_text())
        data_list.append(data)
    if len(data_list) == 0:
        return ("No data was found for this customer, return a final answer that you are not able to find "
                "this information")
    response = (json.dumps(data_list))
    return response

class JSONLoadInput(BaseModel):
    account_number: Optional[str] = Field(description="Strictly string value of 9 digit, e.g. 123456789, "
                                                      "pass 1234 if not exist")

class JSONLoadTool(BaseTool):
    name = "JSONLoad"
    description = ("useful for getting customer documents in a list of JSON"
                   "Each JSON represent a physical pdf document and could contain multiple pages"
                   "For each page, there are page_number, page_text and file_path information")
    args_schema: Type[BaseModel] = JSONLoadInput

    def _run(
            self,
            account_number = None,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool"""
        return load_json(account_number)


    async def _arun(
            self,
            account_number = None,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return load_json(account_number)