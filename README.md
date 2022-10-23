# Wikipedia Edits Chart

**The API can't be used for now, as it's not uploaded into any web server.**

This is a little program that prints a chart, in the form of a calendar (based
on the year you choose), that shows the days a specified user contributed to a
specific Wikipedia project (that is, a specific Wikipedia language) and the
quantity of the edits they made in that day. The API also counts the total
amount of edits made in a year and the current (for the current year) or the
longest (for any other year) streak of edits. Head to the [Example](#example)
section to see how does it look. **The contribution chart from GitHub was my inspiration.**

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

## Example

<img alt="WikipediaEditsChart example in light mode" src="https://user-images.githubusercontent.com/37962411/197352254-ced67731-235d-4a14-9bbc-97e0f85f6774.png" title="In light mode" height="420"/>
<img alt="WikipediaEditsChart example in dark mode" src="https://user-images.githubusercontent.com/37962411/197353347-404a9148-8ac0-452c-8276-e14cc5109f38.png" title="In dark mode" height="409"/>

## Usage

To get the chart, simply go to **https://wikipedia-edits-chart.glitch.me** and
add the required parameters. Below you can find the list of the available path
and query parameters, as well as some examples.

### List of parameters

| Parameter      | Type            | Example                                                               | Required |
| ----------     | --------------- | --------------------------------------------------------------------- | -------- |
| username       | path parameter  | https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales                 | yes      |
| language[^1]   | query parameter | https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?language=en     | yes      |
| year           | query parameter | https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?year=2022       | yes      |
| appearance[^2] | query parameter | https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?appearance=dark | no       |

### List of examples

- See the edits from Jimbo Wales in the English Wikipedia in 2020:
    - https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?language=en&year=2020
- See the edits from Jimbo Wales in the English Wikipedia in 2022 in dark mode:
    - https://wikipedia-edits-chart.glitch.me/Jimbo%20Wales?language=en&year=2022&appearance=dark

## Remarks

[^1]: Wikipedia is available in [many languages](https://meta.wikimedia.org/wiki/List_of_Wikipedias). Wikimedia uses a combination of standards to define the language codes. Here is a [list of language codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for you to know.
[^2]: The default value is "light". You can specify it explicitly or leave it. If you want the dark mode, you need to specify it explicitly.
