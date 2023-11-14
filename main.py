from fastapi import FastAPI, HTTPException, Body
from datetime import datetime
from typing import Any
import content_generator
from dotenv import find_dotenv, load_dotenv

app = FastAPI()
_ = load_dotenv(find_dotenv())
assistant = content_generator.ContentGenerator()


@app.post("/doc", status_code=201)
async def send_programming_docs(payload: Any = Body(None)):
    # ...
    try:
        print("Sending request to GPT")
        response = await assistant.get_openai_response(payload)
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"Tests/{current_datetime}", "w") as test_file:
            test_file.write(response)
        return {"response": "results saved in file"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
