from ast import match_case
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
        "ucuser": username,
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
        contrib_data += f"<div id=\"{month_names[month_count]}\" class=\"month\">"
        contrib_data += f"<p class=\"month-title\">{month_names[month_count]}</p>"
        contrib_data += "<div class=\"month-container\">"

        week_count = 1
        for week in month:
            contrib_data += f"<div id=\"Week {week_count}\" class=\"week\">"

            for day in week:
                full_day = f"{year}-{str(month_count).zfill(2)}-{str(day).zfill(2)}"
                repr_day = f"{month_names[month_count][:3]} {day}, {year}"

                day_transparency = ""
                contrib_level = "day-level-0"
                tooltip = f"title=\"No contributions on {repr_day}\""

                if day == 0:
                    day_transparency = "yes-transparent"
                    tooltip = ""

                if full_day in contrib_days:
                    tooltip = f"title=\"{contrib_days[full_day]} contributions on {repr_day}\""

                    if contrib_days[full_day] >= 50:
                        contrib_level = "day-level-5"
                    elif contrib_days[full_day] >= 30:
                        contrib_level = "day-level-4"
                    elif contrib_days[full_day] >= 15:
                        contrib_level = "day-level-3"
                    elif contrib_days[full_day] >= 5:
                        contrib_level = "day-level-2"
                    elif contrib_days[full_day] >= 2:
                        contrib_level = "day-level-1"
                    elif contrib_days[full_day] == 1:
                        contrib_level = "day-level-1"
                        tooltip = f"title=\"{contrib_days[full_day]} contribution on {repr_day}\""

                contrib_data += f"<div class=\"day {day_transparency} {contrib_level}\" {tooltip}></div>"

            contrib_data += "</div>"
            week_count += 1

        contrib_data += "</div>"
        contrib_data += "</div>"
        month_count += 1

    return templates.TemplateResponse(
        "userchart.html",
        {
            "request": request,
            "year": year,
            "username": username,
            "data": contrib_data
        }
    )