# SW QA Assistant (FastAPI Application with LLM Integration)

## Introduction

This application is a FastAPI backend service that you communicate with through REST API endpoints at `http://127.0.0.1:8000`
1) `/generate` endpoint will write test cases based on the documentation you send it (e.g. API definition or a page's html)
2) By default, those tests are written using cypress. You can change that to playwright or selenium with a POST to `/framework`
3) When tests fail, find clues on breaking commits by sending a txt test report to `/analyze`. Requires that your code is hosted on github

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
   Fill out your env variables in the .env file. An OpenAI key is mandatory.
   You can run the application from the main.py file.

3. **Containerization**
   
   Dockerfile is provided if you want to run the app in its own container
   ```bash
   docker build -t qa-agent .
   docker run -d --name agent -p 8000:8000 --env-file .env  -v $(pwd)/GPT_GENERATED_CONTENT:/usr/src/app/GPT_GENERATED_CONTENT qa-agent


## Using the application
**Writing test cases**

1. Send the documentation you want to base the tests on to the
   `/generate` endpoint on port 8000. Response will be saved in the /GPT_GENERATED_CONTENT folder

```
curl -X POST -F "file=@petstore_sample.txt" "http://127.0.0.1:8000/generate"
```

The default framework is cypress. You can change this to playwright or selenium with the `/framework` endpoint
```
{"framework":"playwright"}
```

There's a sample `petstore_sample.txt` file with an API definition you can send to `http://127.0.0.1:8000/generate` to confirm the app has been deployed correctly. Tests should be stored in the /GPT_GENERATED_CONTENT folder.

**Checking for breaking commits**

1. Set the env variables GIT_USER & GIT_REPO
2. Send a test report in text format to the `/analyze` endpoint

```
curl -X POST -F "file=@output.txt" "http://127.0.0.1:8000/analyze?days=21"
```
The `days`param is how far back you want to check the repo. Default is 1 (changes in the last 24 hours)

App will compare the test report with the information it got from GitHub, and point out
breaking changes. Note that there may be rate limiting on GitHub's part
