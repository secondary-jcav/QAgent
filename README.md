# FastAPI Application with OpenAI Integration

## Introduction

This application is a FastAPI backend service designed to receive your app's html or API definition through a REST API endpoint on http://127.0.0.1:8000/doc and generate Cypress test cases using OpenAI's GPT-4 model. The prompt is defined in content_generator.py

```
"You're an expert software engineer. You receive program documentation and provide Cypress tests to validate it" \
                      "If you receive an API doc in the OpenAPI standard, you will provide functional API tests using cypress that cover all the endpoints detailed in the API doc." \
                      "If you receive an html, you will provide E2E cypress tests that cover the locators and attributes present in the file." \
                      "It's important that your response covers every endpoint or selector describen in the documentation you receive"
```

## Prerequisites

- Docker (optional)
- An OpenAI API key

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/secondary-jcav/QAgent.git
   cd QAgent
   pip install -r requirements.txt

2. **Local Execution**   
   Write your OpenAI key in the .env file.
   You can run the application with the uvicorn command.
   Send the documentation you want to base the tests on to the
   /doc endpoint on port 8000. They will be saved in the /Tests folder
   ```bash
   uvicorn main:app --reload

3. **Containerization**
   
   Dockerfile is provided if you want to run the app in its own container
   ```bash
   docker build -t qa-agent .
   docker run -d --name testwriter -p 8000:8000 -e OPENAI_API_KEY='Your-OpenAI-API-Key' -v $(pwd)/Tests:/usr/src/app/Tests qa-agent
