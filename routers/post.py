from datetime import datetime
from fastapi import APIRouter, Body, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from typing import Any
from github.github_client import GithubClient
from llm.test_writer import TestWriter
from llm.bug_finder import ReportChecker


router = APIRouter()

inspector = ReportChecker()
test_writer = TestWriter()
repo_diver = GithubClient()


stored_framework = "cypress"  # default value


class FrameworkModel(BaseModel):
    framework: str

    @validator('framework')
    def validate_framework(cls, v):
        if v.lower() not in ["cypress", "playwright", "selenium"]:
            raise ValueError("Invalid framework value. Must be 'cypress', 'playwright', or 'selenium'.")
        return v.lower()


@router.post("/framework", status_code=201)
async def store_framework(framework: FrameworkModel):
    global stored_framework
    stored_framework = framework.framework
    return {"message": f"Framework '{stored_framework}' stored successfully"}


@router.post("/generate", status_code=201)
async def send_programming_docs(file: UploadFile = File(...)):
    # Send documentation to LLM endpoint to generate test cases
    if file.content_type != 'text/plain':
        return JSONResponse(status_code=400, content={"message": "This endpoint only accepts text/plain files."})

    try:
        if stored_framework is None:
            raise ValueError("Invalid framework value. Must be 'cypress', 'playwright', or 'selenium'.")
        content = await file.read()
        payload = content.decode("utf-8")
        print(f"Sending request to GPT for {stored_framework} tests")
        response = await test_writer.write_test(payload, stored_framework)
        print("writing response to /GPT_GENERATED_CONTENT")

        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"GPT_GENERATED_CONTENT/{current_datetime}", "w") as test_file:
            test_file.write(response)
        return {"response": "results saved in file"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze", status_code=201)
async def upload_test_report(file: UploadFile = File(...), days: int = Query(1)):
    # Receives a test report and compares with latest git commits to find the culprit
    await repo_diver.start_session()
    if file.content_type != 'text/plain':
        return JSONResponse(status_code=400, content={"message": "This endpoint only accepts text/plain files."})
    try:
        content = await file.read()
        test_report = content.decode("utf-8")
        timestamp = repo_diver.get_timestamp(days)
        print(timestamp)
        latest_commits = await repo_diver.get_latest_commits(timestamp)
        if not latest_commits:
            return {"response": f"No commits found in the last {days} day(s)"}

        commit_report = ""
        for commit in latest_commits:
            commit_report += await repo_diver.get_commit_info(commit)

        breaking_changes = inspector.test_result_analysis(test_report, commit_report)
        print(breaking_changes)
        return {"breaking changes": breaking_changes}
    finally:
        await file.close()
        await repo_diver.close_session()
