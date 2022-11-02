import requests
import calendar
from datetime import datetime, timedelta
import json
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
    
    if year == "current":
        year = str(datetime.now().year)

    r_url = f"https://{language}.wikipedia.org/w/api.php"
    r_params = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "uclimit": 500,
        "ucuser": username,
        "ucstart": f"{year}-12-31T00:00:00Z",
        "ucend": f"{year}-01-01T00:00:00Z"
    }

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

    month_names, language_codes = get_external_data()
    edit_days, edit_count = get_edit_days(response, r_url, r_params)
    streak_edits = calculate_streak(year, edit_days)
    day_levels = get_day_levels(edit_days)

    full_lang = language
    if language in language_codes:
        full_lang = language_codes[language]

    colour_mode = f"/{appearance}.css"

    edit_data = format_data_html(
        username, year, month_names, edit_days, day_levels,
        full_lang, edit_count, streak_edits, colour_mode
    )

    return edit_data


def get_external_data() -> tuple:
    """Reads the "external.json" file and retrieves their objects

    Returns
    -------
    tuple[dict, dict]
        two dicts, one with the map between numbers and month names
        and other with the map between language codes and full language
        names
    """

    with open("external.json", "r") as json_read:
        json_data = json.load(json_read)

    return json_data["month-names"], json_data["language-codes"]


def get_edit_days(response: dict, r_url: str, r_params: str) -> tuple:
    """Retrieves the days of edits and the number of edits

    Parameters
    ----------
    response : dict
        The first response taken from the Mediawiki Action API
    r_url : str
        The URL of the response
    r_params : str
        The parameters to attach to the response

    Returns
    -------
    tuple[dict, int]
        a dict with the dates the user made at least one edit and the
        quantity of the edits and a number with the total count of
        edits made
    """

    edit_days = {}

    while 1:
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

    edit_count = sum(edit_days.values())

    return edit_days, edit_count


def calculate_streak(year: str, edit_days: dict) -> str:
    """Calculates de current or the longest streak made

    Parameters
    ----------
    year : str
        The year the user chose
    edit_days : dict
        The dict with the days and count of edits the user made
        for each of them

    Returns
    -------
    str
        the text with the number of the current or the longest
        streak
    """

    streak_number = 0
    streak_edits = ""

    if year == str(datetime.now().year):
        last = datetime.now()
        while 1:
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

    return streak_edits


def get_day_levels(edit_days: dict) -> list:
    """Calculates the numbers to use as breakpoints for the colours

    Parameters
    ----------
    edit_days : dict
        The dict with the days and count of edits the user made
        for each of them

    Returns
    -------
    list
        the numbers that the HTML classes should use to decide
        which tone of colour to apply to the square
    """

    day_levels = []
    max_edit = max(edit_days.values())
    last_number = max_edit

    for _ in range(5):
        last_number = last_number - (max_edit / 6)
        day_levels.append(int(last_number))

    return day_levels


def format_data_html(
        username: str, year: str, month_names: dict, edit_days: dict, day_levels: list,
        full_lang: str, edit_count: str, streak_edits: str, colour_mode: str
    ) -> str:
    """Formats the data using HTML tags and attributes

    Parameters
    ----------
    year : str
        The year the user chose
    month_names : dict
        A dict with the map between numbers and month names
    edit_days : dict
        The dict with the days and count of edits the user made
        for each of them
    day_levels : list
        List of numbers to serve as breakpoints for the colours
        of the squares

    Returns
    -------
    str
        the HTML string with all the information
    """

    edit_data = f"""
    <svg xmlns=\"http://www.w3.org/2000/svg\" width=\"627\" height=\"404\">
        <link rel=\"stylesheet\" href=\"static/global.css\" type=\"text/css\" />
        <rect x=\"0.5\" y=\"0.5\" rx=\"6\" width=\"626\" height=\"99%\" stroke=\"#b3b3b3\" stroke-width=\"2\" fill=\"#ffffff\">
            <rect x=\"10\" y=\"10\" rx=\"6\" width=\"620\" height=\"90%\" stroke=\"#ebebeb\" stroke-width=\"6\" fill=\"#ffffff\">
            <g id=\"user-and-year\">
                <text>Edits from {username} in {year}</text>
            </g>
            <g id=\"year-container\">
    """
    year_days = calendar.Calendar().yeardayscalendar(int(year), width=12)

    month_count = 1
    for month in year_days[0]:
        lower_month = month_names[str(month_count)].lower()

        edit_data += f"""
        <g id=\"{lower_month}\" class=\"month\">
            <text class=\"month-title\">{month_names[str(month_count)]}</text>
            <g class=\"month-container\">
        """

        week_count = 1
        for week in month:
            edit_data += f"<g id=\"{lower_month}-week-{week_count}\" class=\"week\">"

            for day in week:
                number_day = f"{year}-{str(month_count).zfill(2)}-{str(day).zfill(2)}"
                char_day = f"{month_names[str(month_count)][:3]} {day}, {year}"

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
                <rect rx=\"2\" width=\"14\" height=\"14\" title=\"{tooltip}\" class=\"day {edit_level} {day_transparency}\"/>
                """

            edit_data += "</g>"
            week_count += 1

        edit_data += """
            </g>
        </g>
        """
        month_count += 1

    edit_data += f"""
                </g>
                <g id=\"additional-info\" transform=\"translate(300, 390)\">
                    <g id=\"project-language\">
                        <svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 576 512\" width=\"30\" height=\"26.666\" title=\"The language of the Wikipedia project\"><path d=\"M565.6 36.24C572.1 40.72 576 48.11 576 56V392C576 401.1 569.8 410.9 560.5 414.4L392.5 478.4C387.4 480.4 381.7 480.5 376.4 478.8L192.5 417.5L32.54 478.4C25.17 481.2 16.88 480.2 10.38 475.8C3.882 471.3 0 463.9 0 456V120C0 110 6.15 101.1 15.46 97.57L183.5 33.57C188.6 31.6 194.3 31.48 199.6 33.23L383.5 94.52L543.5 33.57C550.8 30.76 559.1 31.76 565.6 36.24H565.6zM48 421.2L168 375.5V90.83L48 136.5V421.2zM360 137.3L216 89.3V374.7L360 422.7V137.3zM408 421.2L528 375.5V90.83L408 136.5V421.2z\"/></svg>
                        <text>{full_lang} Wikipedia</text>
                    </g>
                    <g id=\"total-contribution\">
                        <svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 3.349 3.826\" width=\"25\" height=\"28.571\" title=\"Total amount of edits in the year\"><path d=\"M1.136 0.479h1.076V0.179a0.179 0.179 0 1 1 0.359 0v0.299h0.299c0.264 0 0.479 0.214 0.479 0.479v2.391a0.479 0.479 0 0 1 -0.479 0.479H0.479A0.479 0.479 0 0 1 0 3.349v-2.391C0 0.693 0.214 0.479 0.479 0.479h0.299V0.179a0.179 0.179 0 1 1 0.359 0v0.299zM0.359 3.349c0 0.066 0.054 0.119 0.119 0.119h2.391a0.119 0.119 0 0 0 0.119 -0.119V1.435H0.359v1.914z\"/></svg>
                        <text>Total edits: {edit_count}</text>
                    </g>
                    <g id=\"current-streak\">
                        <svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 32 28.444\" width=\"32\" height=\"28.444\" title=\"Longest or current streak of edits\"><path d=\"M15.994 0c0.511 0 0.978 0.292 1.2 0.752l3.811 7.849 8.518 1.261c0.5 0.072 0.912 0.423 1.072 0.9 0.156 0.484 0.028 1.011 -0.328 1.36L24.088 18.244l1.46 8.639c0.083 0.5 -0.121 1.011 -0.538 1.305 -0.41 0.295 -1.006 0.333 -1.405 0.095l-7.61 -4.067 -7.656 4.067c-0.4 0.24 -0.944 0.2 -1.36 -0.095 -0.41 -0.295 -0.617 -0.806 -0.584 -1.305l1.505 -8.639L1.728 12.121c-0.359 -0.349 -0.487 -0.878 -0.329 -1.36 0.157 -0.477 0.572 -0.828 1.072 -0.9l8.512 -1.261 3.811 -7.849C15.022 0.292 15.482 0 15.994 0zm0 4.387L13.078 10.4c-0.195 0.394 -0.572 0.672 -1.006 0.739L5.498 12.105 10.272 16.833c0.306 0.306 0.444 0.745 0.372 1.172l-1.123 6.644 5.844 -3.122c0.394 -0.211 0.867 -0.211 1.256 0l5.844 3.122 -1.123 -6.644c-0.072 -0.428 0.072 -0.867 0.377 -1.172l4.772 -4.728 -6.573 -0.967c-0.439 -0.067 -0.816 -0.344 -1.006 -0.739L15.994 4.387z\"/></svg>
                        <text>{streak_edits}</text>
                    </g>
                </g>
            </rect>
        </rect>
    </svg>
    """

    return edit_data
