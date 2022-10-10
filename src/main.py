from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/{username}", response_class=HTMLResponse)
async def get_user(username: str, language: str, timezone: str = "UTC"):
    return f"""
    Hello, {username}. {language}, {timezone}
    """