import requests
import calendar
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/{username}", response_class=HTMLResponse)
async def get_user(request: Request, username: str, language: str, year: str):
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

    # Request and save the data
    response = None
    try:
        response = requests.get(url=r_url, params=r_params).json()
    except:
        print("The user couldn't be found.")

    if len(response["query"]["usercontribs"]) == 0:

        return templates.TemplateResponse(
            "userchart.html",
            {
                "request": request,
                "year": year,
                "username": username,
                "data": "<p id=\"not-found\">No data was found for this period of time.</p>"
            }
        )

    contrib_days = {}
    while True:
        for contribution in response["query"]["usercontribs"]:
            date = contribution["timestamp"][:10]

            if date not in contrib_days.keys():
                contrib_days[date] = 1
            else:
                contrib_days[date] = contrib_days[date] + 1

        if "continue" not in response:
            break

        r_params["uccontinue"] = response["continue"]["uccontinue"]
        response = requests.get(url=r_url, params=r_params).json()

    max_contrib = max(contrib_days.values())
    day_levels = []
    last_number = max_contrib
    for _ in range(5):
        last_number = last_number - (max_contrib / 6)
        day_levels.append(int(last_number))

    # Format the data using HTML
    contrib_data = ""

    year_days = calendar.Calendar().yeardayscalendar(int(year), width=12)
    
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
                number_day = f"{year}-{str(month_count).zfill(2)}-{str(day).zfill(2)}"
                char_day = f"{month_names[month_count][:3]} {day}, {year}"

                day_transparency = ""
                contrib_level = "day-level-0"
                tooltip = f"No contributions on {char_day}"

                if day == 0:
                    day_transparency = "yes-transparent"
                    tooltip = ""

                if number_day in contrib_days:
                    tooltip = f"{contrib_days[number_day]} contributions on {char_day}"

                    if contrib_days[number_day] >= day_levels[0]:
                        contrib_level = "day-level-6"
                    elif contrib_days[number_day] >= day_levels[1]:
                        contrib_level = "day-level-5"
                    elif contrib_days[number_day] >= day_levels[2]:
                        contrib_level = "day-level-4"
                    elif contrib_days[number_day] >= day_levels[3]:
                        contrib_level = "day-level-3"
                    elif contrib_days[number_day] >= day_levels[4]:
                        contrib_level = "day-level-2"
                    elif contrib_days[number_day] < day_levels[4] and contrib_days[number_day] > 1:
                        contrib_level = "day-level-1"
                    elif contrib_days[number_day] == 1:
                        contrib_level = "day-level-1"
                        tooltip = f"{contrib_days[number_day]} contribution on {char_day}"

                contrib_data += f"""
                <div class=\"day {day_transparency} {contrib_level}\">
                    <span class=\"tooltip-text\">{tooltip}</span>
                </div>
                """

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