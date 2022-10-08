from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return "test"


@app.get("/{username}/{language}")
async def get_user(username: str, language: str):
    return f"Hello, {username}. You are in the {language} Wikipedia"