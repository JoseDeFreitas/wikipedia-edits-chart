# Wikipedia Edits Chart

This is a small program that prints a chart, in the form of a calendar (based
on the year you choose),[^1] that shows the days a specified user contributed to
a specific Wikipedia project (that is, a specific Wikipedia language) and the
amount of edits they made in that day. The program also counts the total
amount of edits made in the year and the streak of edits.[^2] Head to the
[Screenshots](#screenshots) section to see how it looks. **The contribution
chart from GitHub was my inspiration.**

Charts like this exist in some websites. Although they look cool, I don't think
they provide anything useful, and, in some cases, I believe they're noxious as
force you to keep contributing (even if you don't want to) or preserve a streak
that is, pretty much, useless. This may not seem like an issue, but I do believe
it's wrong to make a change (in any website) just to keep the chart "pretty".

I didn't code this program for people to make it part of their contribution schedule
to Wikipedia, where what people should do is contribute when they have something
good to provide.

## Screenshots

<a href="https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales/en?year=2021"><img alt="Wikipedia Edits Chart example in light mode" src="https://user-images.githubusercontent.com/37962411/198012135-e72aa9fd-1035-44b7-bf74-3298720bf26f.png" title="In light mode" height="404"/></a>
<a href="https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales/en?year=2022&theme=dark"><img alt="Wikipedia Edits Chart example in dark mode" src="https://user-images.githubusercontent.com/37962411/198012209-8b561a39-2841-4aad-a57a-61f42e23c13d.png" title="In dark mode" height="393"/></a>

## Usage

To get the chart, simply go to **https://wikipedia-edits-chart.glitch.me** and
add the required parameters. Below you can find the list of the available path
and query parameters, as well as some examples. If the user couldn't be found or
there are no edits for the choosen year, the website will let you know with a red
message.

To see the amount of katas completed in a day, you must hover over that day.

### Parameters

| Parameter          | Required | Default value    |
| ------------------ | -------- | ---------------- |
| username           | yes      |                  |
| language[^3]       | yes      |                  |
| year               | no       | Current year     |
| theme              | no       | light            |

### Examples

- See the edits from Jimbo Wales in the English Wikipedia in 2020:
    - https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales/en?year=2020
- See the edits from Jimbo Wales in the English Wikipedia in 2022 in dark mode:
    - https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales/en?year=2022&theme=dark

## Remarks

- The limit of edits to retrieve is 500 per request, as stated in the
["Usercontribs" API section](https://www.mediawiki.org/wiki/API:Usercontribs) of
the [Mediawiki Action API](https://www.mediawiki.org/wiki/API:Main_page).
The output JSON contains a value that you can use to continue the retrieval of
the data if the number of edits exceeds the limit; however, it has to make another
request, and, because the program loops one by one through all of the edits
(as [Wikimedia asks you to not make the requests in parallel](https://www.mediawiki.org/wiki/API:Etiquette)),
it may take some seconds for users that have made many edits. Based on some
requests I made, it takes roughly 500ms per 1000 edits. **Please, don't overwhelm
the website**.
- When no one has made a request to the website in 5 minutes, Glitch (the host
I'm using) turns off the website. In this case, you'll need to wait some seconds for
the chart to appear. There is also a [limited amount of hours per month](https://help.glitch.com/kb/article/17-technical-restrictions/)
for the free plan (which is the one I'm using).
- The timezone used by the program is **UTC**. This is because it's faster this way
for the user to get the chart (as he would need to also type in the timezone they
want). However, I may introduce the feature to select a specific timezone in the
future.

[^1]: The shape of the months are different from one another because, instead of
printing the days as GitHub does, it prints them like a normal calendar. You can
see the day of the week by counting the row the day is in. It starts at Monday and
finishes at Sunday.
[^2]: If you choose the current year, it will print the current streak. If you
choose any other year that has already passed, it will print the longest streak
made.
[^3]: Wikipedia is available in [many languages](https://meta.wikimedia.org/wiki/List_of_Wikipedias).
Wikimedia uses a combination of standards to define the language codes. Here is a
[list of language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for you to know.
