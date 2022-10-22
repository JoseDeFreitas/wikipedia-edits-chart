# WikipediaEditsChart

**The API can't be used for now, as it's not uploaded into any web server.**

This is a little program that prints a chart, in the form of a calendar (based
on the year you select), that shows the days a specified user contributed to a
specific Wikipedia project (that is, a specific Wikipedia language) and the
quantity of the edits they made in that current day. The API also counts the
total amount of edits made in a year and the current (for the current year) or
the longest (for any other year) streak of edits. Head to the [Example](#example)
section to see how does it look. **The contribution chart from GitHub was my inspiration.**

Charts like this exist in some websites. Although they look cool, I don't think
they provide anything useful, and, in some cases, I believe they're noxious as
force you to keep contributing (even if you don't want to) or preserve the streak,
that is useless and serves only for you to say "Oh, this looks pretty". This
may not seem like an issue, but I do believe it's wrong to make a change (in
any website) just to keep the chart "pretty". It's not that of a big deal as
it's on you to not pay attention to the chart and stop doing any useless
change, but it's still an incentive to do this.

I didn't make this API for people to make it a part of their contribution
schedule to Wikipedia, where what people should do is contribute when they have
something good to provide. It's counter-intuitive creating a project like this
when you don't especially like it. However, here it is. I can't say it doesn't
look cool.

## Example

![WikipediaEditsChart example in light mode](https://user-images.githubusercontent.com/37962411/197352254-ced67731-235d-4a14-9bbc-97e0f85f6774.png "In light mode")
![WikipediaEditsChart example in dark mode](https://user-images.githubusercontent.com/37962411/197352275-e405b1fc-3d49-4a4f-b95c-2165ffad44c6.png "In dark mode")

## Usage

To get the chart, simply go to **[INSERT website name]**. Below you can find the
list of the available path and query parameters, as well as some examples.

### List of parameters

| Parameter  | Type            | Example                               | Required | Default |
| ---------- | --------------- | ------------------------------------- | -------- | ------- |
| username   | path parameter  | [website]/Jimbo Wales                 | yes      | none    |
| language   | query parameter | [website]/Jimbo Wales?language=en     | yes      | none    |
| year       | query parameter | [website]/Jimbo Wales?year=2022       | yes      | none    |
| appearance | query parameter | [website]/Jimbo Wales?appearance=dark | no       | light   |

### List of examples

- See the contributions from Jimbo Wales in the English Wikipedia in 2020:
    - [website]/Jimbo Wales?language=en&year=2020
- See the edits from Jimbo Wales in the English Wikipedia in 2022 in dark mode:
    - [website]/Jimbo Wales?language=en&year=2020&appearance=dark

## Remarks
