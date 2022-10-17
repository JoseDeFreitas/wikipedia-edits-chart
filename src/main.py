import requests
import calendar
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/{username}", response_class=HTMLResponse)
async def get_user(request: Request, username: str, language: str, year: str):
    URL = f"https://{language}.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "uclimit": 500,  # maximum allowed to request
        "ucuser": username
    }

    # Request and save the data
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

    # Format the data using HTML
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

    return templates.TemplateResponse(
        "userchart.html",
        {
            "request": request,
            "id": id,
            "year": year,
            "username": username,
            "data": contrib_data
        }
    )