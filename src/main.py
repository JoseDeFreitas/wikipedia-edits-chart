from fastapi import FastAPI

app = FastAPI()


@app.get("/{username}")
async def get_user(username: str, language: str, timezone: str = "UTC"):
    return f"Hello, {username}. {language}, {timezone}"