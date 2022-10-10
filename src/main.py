import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/{username}", response_class=HTMLResponse)
async def get_user(username: str, language: str):
    URL = f"https://{language}.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "uclimit": 500,
        "ucuser": username
    }

    response = requests.get(url=URL, params=PARAMS).json()

    for contribution in response["query"]["usercontribs"]:
        date = contribution["timestamp"][:10]

    return f"""
    Hello, {username}. {language}
    """