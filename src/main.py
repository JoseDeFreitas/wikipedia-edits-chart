import requests
import calendar
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/{username}", response_class=HTMLResponse)
async def get_user(username: str, language: str, year: str):
    URL = f"https://{language}.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "uclimit": 500,  # maximum allowed to request
        "ucuser": username
    }

    response = None
    try:
        response = requests.get(url=URL, params=PARAMS).json()
    except:
        print("The user couldn't be found.")

    contrib_days = {}
    for contribution in response["query"]["usercontribs"]:
        date = contribution["timestamp"][:10]

        if date not in contrib_days.keys():
            contrib_days[date] = 1
        else:
            contrib_days[date] = contrib_days[date] + 1

    contrib_data = ""

    days_y = calendar.Calendar().yeardayscalendar(2022, width=12)
    for month in days_y[0]:
        for week in month:
            for i in range(7):
                contrib_data += f"{week[i]}"

    return f"""
    <body>
        <h1>Year: {year}. Contributions from user {username}</h1>
        <div id="contribution-chart">
            {contrib_data}
        </div>
    </body>
    """