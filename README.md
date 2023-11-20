# FastAPI Application with OpenAI Integration

## Introduction

This application is a FastAPI backend service designed to receive documents through a REST API endpoint on http://127.0.0.1:8000/doc and generate Cypress test cases using OpenAI's GPT-4 model. It's an ideal setup for automatically generating test cases for API and HTML documentation.

## Prerequisites

- Docker
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
   docker build -t fastapi-app .
   docker run -d --name myfastapiapp -p 8000:8000 -e OPENAI_API_KEY='Your-OpenAI-API-Key' -v $(pwd)/Tests:/usr/src/app/Tests fastapi-app
