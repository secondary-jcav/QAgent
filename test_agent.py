import asyncio
import content_generator
from dotenv import find_dotenv, load_dotenv

# Tests basic functionality
_ = load_dotenv(find_dotenv())
assistant = content_generator.ContentGenerator()

FILE_SAMPLE = 'petstore_simple.json'

with open(FILE_SAMPLE, 'r') as file:
    data = file.read()
    tests = asyncio.run(assistant.get_openai_response(data, "cypress"))
    assert "describe" in tests
    assert "it" in tests
    print(tests)
