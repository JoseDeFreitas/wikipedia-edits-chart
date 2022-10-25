import requests
import calendar
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/{username}", response_class=HTMLResponse)
async def get_user(
    request: Request, username: str, language: str,
    year: str, appearance: str = "light"
    ):
    r_url = f"https://{language}.wikipedia.org/w/api.php"
    r_params = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "uclimit": 500,  # maximum allowed to request
        "ucuser": username,
        "ucstart": f"{year}-12-31T00:00:00Z",
        "ucend": f"{year}-01-01T00:00:00Z"
    }

    colour_mode = f"/{appearance}.css"

    # Request and save the data
    response = None
    try:
        response = requests.get(url=r_url, params=r_params).json()
    except:
        print("There was a problem while connecting to the API.")
        return

    if len(response["query"]["usercontribs"]) == 0:
        return templates.TemplateResponse(
            "nodata.html",
            {
                "request": request,
                "data": "<p id=\"not-found\">No data was found for this user for this period of time.</p>",
            }
        )

    edit_days = {}
    while True:
        for contribution in response["query"]["usercontribs"]:
            date = contribution["timestamp"][:10]

            if date not in edit_days.keys():
                edit_days[date] = 1
            else:
                edit_days[date] = edit_days[date] + 1

        if "continue" not in response:
            break

        r_params["uccontinue"] = response["continue"]["uccontinue"]
        response = requests.get(url=r_url, params=r_params).json()

    # Calculate total number of edits in the year
    edit_count = sum(edit_days.values())

    # Calculate longest and current streak
    streak_number = 0
    streak_edits = ""

    if year == str(datetime.now().year):
        last = datetime.now()
        while True:
            if str(last)[:10] in edit_days:
                streak_number += 1
                last = last - timedelta(days=1)
            else:
                break

        streak_edits = f"Current streak: {streak_number}"
    else:
        streak_count = 0
        last = datetime.strptime(list(edit_days.keys())[0], "%Y-%m-%d")
        for day in range(len(list(edit_days.keys()))):
            if str(last)[:10] in edit_days:
                streak_count += 1
                last = last - timedelta(days=1)

                if (streak_number < streak_count):
                    streak_number = streak_count
            else:
                last = datetime.strptime(list(edit_days.keys())[day], "%Y-%m-%d") - timedelta(days=1)
                streak_count = 1

        streak_edits = f"Longest streak: {streak_number}"

    # Create list with breakpoints for the colours of the squares
    max_edit = max(edit_days.values())
    day_levels = []
    last_number = max_edit
    for _ in range(5):
        last_number = last_number - (max_edit / 6)
        day_levels.append(int(last_number))

    # Format the data using HTML
    edit_data = ""
    year_days = calendar.Calendar().yeardayscalendar(int(year), width=12)
    month_names = {
        1: "January", 2: "February", 3: "March",
        4: "April", 5: "May", 6: "June",
        7: "July", 8: "August", 9: "September",
        10: "October", 11: "November", 12: "December"
    }

    month_count = 1
    for month in year_days[0]:
        lower_month = month_names[month_count].lower()

        edit_data += f"<div id=\"{lower_month}\" class=\"month\">"
        edit_data += f"<h2 class=\"month-title\">{month_names[month_count]}</h2>"
        edit_data += "<div class=\"month-container\">"

        week_count = 1
        for week in month:
            edit_data += f"<div id=\"{lower_month}-week-{week_count}\" class=\"week\">"

            for day in week:
                number_day = f"{year}-{str(month_count).zfill(2)}-{str(day).zfill(2)}"
                char_day = f"{month_names[month_count][:3]} {day}, {year}"

                day_transparency = "no-transparent"
                edit_level = "day-level-0"
                tooltip = f"No contributions on {char_day}"

                if day == 0:
                    day_transparency = "yes-transparent"
                    edit_level = ""
                    tooltip = ""

                if number_day in edit_days:
                    tooltip = f"{edit_days[number_day]} contributions on {char_day}"

                    if edit_days[number_day] >= day_levels[0]:
                        edit_level = "day-level-6"
                    elif edit_days[number_day] >= day_levels[1]:
                        edit_level = "day-level-5"
                    elif edit_days[number_day] >= day_levels[2]:
                        edit_level = "day-level-4"
                    elif edit_days[number_day] >= day_levels[3]:
                        edit_level = "day-level-3"
                    elif edit_days[number_day] >= day_levels[4]:
                        edit_level = "day-level-2"
                    elif edit_days[number_day] < day_levels[4] and edit_days[number_day] > 1:
                        edit_level = "day-level-1"
                    elif edit_days[number_day] == 1:
                        edit_level = "day-level-1"
                        tooltip = f"{edit_days[number_day]} contribution on {char_day}"

                edit_data += f"""
                <div class=\"day {edit_level} {day_transparency}\">
                    <span class=\"tooltip-text\">{tooltip}</span>
                </div>
                """

            edit_data += "</div>"
            week_count += 1

        edit_data += "</div>"
        edit_data += "</div>"
        month_count += 1

    return templates.TemplateResponse(
        "userchart.html",
        {
            "request": request,
            "year": year,
            "username": username,
            "data": edit_data,
            "appearance": colour_mode,
            "total": edit_count,
            "streak": streak_edits
        }
    )