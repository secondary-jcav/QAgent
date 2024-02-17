from datetime import datetime
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, validator
from typing import Any
from llm.test_writer import TestWriter


router = APIRouter()
assistant = TestWriter()
stored_framework = "cypress"  # default value


class FrameworkModel(BaseModel):
    framework: str

    @validator('framework')
    def validate_framework(cls, v):
        if v.lower() not in ["cypress", "playwright", "selenium"]:
            raise ValueError("Invalid framework value. Must be 'cypress', 'playwright', or 'selenium'.")
        return v.lower()


@router.post("/framework", status_code=201)
async def store_framework(framework: FrameworkModel):
    global stored_framework
    stored_framework = framework.framework
    return {"message": f"Framework '{stored_framework}' stored successfully"}


@router.post("/generate", status_code=201)
async def send_programming_docs(payload: Any = Body(None)):
    # ...
    try:
        if stored_framework is None:
            raise ValueError("Invalid framework value. Must be 'cypress', 'playwright', or 'selenium'.")

        print(f"Sending request to GPT for {stored_framework} tests")
        response = await assistant.write_test(payload, stored_framework)
        print("writing response to /GPT_GENERATED_CONTENT")

        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"GPT_GENERATED_CONTENT/{current_datetime}", "w") as test_file:
            test_file.write(response)
        return {"response": "results saved in file"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
