import requests
from datetime import datetime, timedelta
import calendar
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

    contrib_days = {}
    for contribution in response["query"]["usercontribs"]:
        date = contribution["timestamp"][:10]

        if date not in contrib_days.keys():
            contrib_days[date] = 1
        else:
            contrib_days[date] = contrib_days[date] + 1

    year_calendar = calendar.HTMLCalendar().formatyear(datetime.now().year, width=4)

    return f"""
    <body>
        <p>{year_calendar}</p>
    </body>
    """