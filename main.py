from fastapi import FastAPI, HTTPException, Body
from datetime import datetime
from typing import Any
import content_generator
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, validator, field_validator

app = FastAPI()
_ = load_dotenv(find_dotenv())
assistant = content_generator.ContentGenerator()

# Global variable to store the framework value
stored_framework = None


class FrameworkModel(BaseModel):
    framework: str

    @validator('framework')
    def validate_framework(cls, v):
        if v.lower() not in ["cypress", "playwright", "selenium"]:
            raise ValueError("Invalid framework value. Must be 'cypress', 'playwright', or 'selenium'.")
        return v.lower()


@app.post("/framework", status_code=201)
async def store_framework(framework: FrameworkModel):
    global stored_framework
    stored_framework = framework.framework
    return {"message": f"Framework '{stored_framework}' stored successfully"}


@app.post("/doc", status_code=201)
async def send_programming_docs(payload: Any = Body(None)):
    # ...
    try:
        print(f"Sending request to GPT for {stored_framework} tests")
        response = await assistant.get_openai_response(payload, stored_framework)
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"Tests/{current_datetime}", "w") as test_file:
            test_file.write(response)
        return {"response": "results saved in file"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
