import requests
import calendar
from datetime import datetime
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

    year_days = calendar.Calendar().yeardayscalendar(datetime.now().year, width=12)
    
    month_names = {
        1: "January", 2: "February", 3: "March",
        4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September",
        10: "October", 11: "November", 12: "December"
    }
    month_count = 1
    for month in year_days[0]:
        contrib_data += f"<div id=\"{month_names[month_count]}\">"
        month_count += 1

        for week in month:
            contrib_data += "<span class=\"Week\">"

            for day in week:
                contrib_data += f"{day}"

            contrib_data += "</span>"

        contrib_data += "</div>"

    return f"""
    <body>
        <h1>Year: {year}. Contributions from user {username}</h1>
        <div id="contribution-chart">
            {contrib_data}
        </div>
    </body>
    """