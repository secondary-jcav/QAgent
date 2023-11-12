import content_generator as bot
from dotenv import find_dotenv, load_dotenv

doc = 'petstore_simple.json'
_ = load_dotenv(find_dotenv())
assistant = bot.ContentGenerator()
with open(doc, 'r') as file:
    data = file.read()
    print(data)
    # tests = assistant.get_openai_response(data)
# with open(f"e2e_test_doc", "w") as test_file:
    # test_file.write(tests)

