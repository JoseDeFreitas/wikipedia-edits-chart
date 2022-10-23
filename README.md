# Wikipedia Edits Chart

This is a little program that prints a chart, in the form of a calendar (based
on the year you choose),[^1] that shows the days a specified user contributed to a
specific Wikipedia project (that is, a specific Wikipedia language) and the
quantity of the edits they made in that day. The API also counts the total
amount of edits made in a year and the streak of edits.[^2] Head to the
[Screenshots](#screenshots) section to see how does it look. **The contribution
chart from GitHub was my inspiration.**

Charts like this exist in some websites. Although they look cool, I don't think
they provide anything useful, and, in some cases, I believe they're noxious as
force you to keep contributing (even if you don't want to) or preserve a streak
that is, pretty much, useless. This may not seem like an issue, but I do believe
it's wrong to make a change (in any website) just to keep the chart "pretty".
It's not that of a big deal as it's up to you not to pay attention to the chart
and stop doing useless changes but it's still an incentive to do so.

I didn't code this API for people to make it part of their contribution schedule
to Wikipedia, where what people should do is contribute when they have something
good to provide. Creating a project that you don't especially like is counter-intuitive.
However, here it is. I can't say it doesn't look cool, to be honest.

## Screenshots

<a href="https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?language=en&year=2021"><img alt="WikipediaEditsChart example in light mode" src="https://user-images.githubusercontent.com/37962411/197352254-ced67731-235d-4a14-9bbc-97e0f85f6774.png" title="In light mode" height="404"/></a>
<a href="https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?language=en&year=2022&appearance=dark"><img alt="WikipediaEditsChart example in dark mode" src="https://user-images.githubusercontent.com/37962411/197353347-404a9148-8ac0-452c-8276-e14cc5109f38.png" title="In dark mode" height="393"/></a>

*You can hover over each day to see the amount of edits in that day*.

## Usage

To get the chart, simply go to **https://wikipedia-edits-chart.glitch.me** and
add the required parameters.[^3] Below you can find the list of the available path
and query parameters, as well as some examples.

### Parameters

| Parameter      | Type            | Example                                                               | Required |
| ----------     | --------------- | --------------------------------------------------------------------- | -------- |
| username       | path parameter  | https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales                 | yes      |
| language[^4]   | query parameter | https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?language=en     | yes      |
| year           | query parameter | https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?year=2022       | yes      |
| appearance[^5] | query parameter | https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?appearance=dark | no       |

### Examples

- See the edits from Jimbo Wales in the English Wikipedia in 2020:
    - https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?language=en&year=2020
- See the edits from Jimbo Wales in the English Wikipedia in 2022 in dark mode:
    - https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?language=en&year=2022&appearance=dark

## Remarks

- The limit of edits to retrieve is 500 per request, as stated in the
["Usercontribs" API section](https://www.mediawiki.org/wiki/API:Usercontribs) of
the [Mediawiki Action API](https://www.mediawiki.org/wiki/API:Main_page).
The output JSON contains a value that you can use to continue the retrieval of
the data if the number of edits exceeds 500; however, it has to make another
request, and, because the program loops one by one through all of the edits
(as [Wikimedia asks you to not make the requests in parallel](https://www.mediawiki.org/wiki/API:Etiquette)),
it may take some seconds for users that have made many edits. Based on some
requests I made, it takes roughly 500ms per 1000 edits. **Please, don't overwhelm
the API**.

[^1]: The shapes of the months are different from one another because, instead of
printing the days as GitHub does, it prints them like a normal calendar. You can
see the day of the week by counting the row the day is in. It starts at Monday and
finishes at Sunday.
[^2]: If you choose the current year, it will print the current streak. If you
choose any other year that has already passed, it will print the longest streak
made.
[^3]: When no one has made a request to the website in 5 minutes, Glitch (the host
I'm using) turns off the website. In this case, you'll need to wait some seconds for
the chart to appear. There is also a [limited amount of hours per month](https://help.glitch.com/kb/article/17-technical-restrictions/)
for the free plan (which is the one I'm using).
[^4]: Wikipedia is available in [many languages](https://meta.wikimedia.org/wiki/List_of_Wikipedias).
Wikimedia uses a combination of standards to define the language codes. Here is a
[list of language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for you to know.
[^5]: The default value is "light". You can specify it explicitly or leave it. If
you want the dark mode, you need to specify it explicitly.
