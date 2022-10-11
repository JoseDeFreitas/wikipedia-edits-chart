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

    days = {}

    for contribution in response["query"]["usercontribs"]:
        date = contribution["timestamp"][:10]

        if date not in days.keys():
            days[date] = 1
        else:
            days[date] = days[date] + 1

    return f"""
    <body>
        <p>{days}</p>
    </body>
    """