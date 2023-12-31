# Test Writing Assistant (FastAPI Application with OpenAI Integration)

## Introduction

This application is a FastAPI backend service designed to receive your app's html or API definition through a REST API endpoint on http://127.0.0.1:8000/generate and output automated test cases using OpenAI's GPT-4 model. The prompt is defined in content_generator.py. You can choose between cypress, playwright or selenium.

```
system_role = f"You're an expert software engineer. You receive program documentation and provide {framework} tests to validate it" \
                      f"If you receive an API doc in the OpenAPI standard, you will provide functional API tests using {framework} that cover all the endpoints detailed in the API doc." \
                      f"If you receive an html, you will provide E2E {framework} tests that cover the locators and attributes present in the file." \
                      f"It's important that your response covers every endpoint or selector describen in the documentation you receive"
```

## Prerequisites

- An OpenAI API key
- Docker (optional)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/secondary-jcav/QAgent.git
   cd QAgent
   pip install -r requirements.txt

2. **Local Execution**   
   Write your OpenAI key in the .env file.
   You can run the application from the main.py file.

3. **Containerization**
   
   Dockerfile is provided if you want to run the app in its own container
   ```bash
   docker build -t qa-agent .
   docker run -d --name testwriter -p 8000:8000 -e OPENAI_API_KEY=Your-OpenAI-API-Key -v $(pwd)/GPT_GENERATED_CONTENT:/usr/src/app/GPT_GENERATED_CONTENT qa-agent


## Using the application
 Send the documentation you want to base the tests on to the
   `/generate` endpoint on port 8000. Response will be saved in the /GPT_GENERATED_CONTENT folder

The default framework is cypress. You can change this to playwright or selenium with the `/framework` endpoint
```
{"framework":"playwright"}
```

There's a sample `petstore_simple.json` file with an API definition you can send to `http://127.0.0.1:8000/generate` to confirm the app has been deployed correctly. Tests should be stored in the /GPT_GENERATED_CONTENT folder.
