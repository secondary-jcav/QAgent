from fastapi import FastAPI

from routers.post import router as post_router

app = FastAPI()
app.include_router(post_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
