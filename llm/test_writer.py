from openai import AsyncOpenAI
from base.base_class import BaseClass


# gets API Key from environment variable OPENAI_API_KEY


class TestWriter(BaseClass):
    def __init__(self):
        super().__init__()
        self.client = AsyncOpenAI()

    async def write_test(self, prompt, framework) -> str:
        """
        Get a response from OpenAI's API.
        """
        system_role = f"You're an expert software engineer. You receive program documentation and provide {framework} tests to validate it" \
                      f"If you receive an API doc in the OpenAPI standard, you will provide functional API tests using {framework} that cover all the endpoints detailed in the API doc." \
                      f"If you receive an html, you will provide E2E {framework} tests that cover the locators and attributes present in the file." \
                      f"It's important that your response covers every endpoint or selector describen in the documentation you receive"
        try:
            completion = await self.client.chat.completions.create(
                model="gpt-4",
                max_tokens=6000,
                messages=[
                    {
                        "role": "system",
                        "content": system_role,
                    },
                    {
                        "role": "user",
                        "content": f"For the provided content, respond with detailed {framework} tests",
                    },
                    {
                        "role": "user",
                        "content": str(prompt)
                    }
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(e)
