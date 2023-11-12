from openai import OpenAI
import asyncio


# gets API Key from environment variable OPENAI_API_KEY


class ContentGenerator:
    def __init__(self):
        self.client = OpenAI()

    def get_openai_response(self, prompt):
        """
        Get a response from OpenAI's API.
        """
        system_role = "You're an expert software engineer. You receive program documentation and provide Cypress tests to validate it" \
        "If you receive an API doc in the OpenAPI standard, you will provide functional API tests using cypress that cover all the endpoints detailed in the API doc." \
        "If you receive an html, you will provide E2E cypress tests that cover the locators and attributes present in the file." \
        "If the documentation you receive is incomplete, you will provide the tests to the best of your ability."
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4",
                max_tokens=6000,
                messages=[
                    {
                        "role": "system",
                        "content": system_role,
                    },
                    {
                        "role": "user",
                        "content": "For the provided content, respond with detailed cypress tests",
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(e)
