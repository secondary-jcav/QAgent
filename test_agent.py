import asyncio
from llm.test_writer import TestWriter

# Tests basic functionality
assistant = TestWriter()

FILE_SAMPLE = 'petstore_simple.json'

with open(FILE_SAMPLE, 'r') as file:
    data = file.read()
    tests = asyncio.run(assistant.write_test(data, "cypress"))
    assert "describe" in tests
    assert "it" in tests
    print(tests)
