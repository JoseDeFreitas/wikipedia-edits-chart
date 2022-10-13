import requests
import pandas as pd
from datetime import datetime, timedelta
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

    full_today = datetime.now()
    cut_today = f"{full_today.year}-{full_today.month}-{full_today.day}"
    all_days = pd.date_range(start=list(contrib_days.keys())[-1], end=cut_today)

    for day in all_days:
        print(str(day)[:10])

    return f"""
    <body>
        <p>{all_days}</p>
    </body>
    """