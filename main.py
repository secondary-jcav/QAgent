from fastapi import FastAPI, Body
from typing import Any
from pydantic import BaseModel
import asyncio
import content_generator as bot
from dotenv import find_dotenv, load_dotenv

app = FastAPI()
doc = 'add-hero-component.html'
_ = load_dotenv(find_dotenv())
assistant = bot.ContentGenerator()


@app.post("/documentation/", status_code=201)
def create_item(payload: Any = Body(None)):
    # simulate some async operation, e.g., saving to a database
    # await asyncio.sleep(1)  # This represents an async operation (e.g., I/O)
    # result = {"name": item.name, "price": item.price}
    # if item.tax:
    #     result["price_with_tax"] = item.price + item.tax
    # Run some other code here
    # ...
    print(payload)
    response = assistant.get_openai_response(payload["doc"])
    print(response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
