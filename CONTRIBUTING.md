# Contributing to Wikipedia Edits Chart

## Add a new translation

The translations of the content into different languages are stored in the [i18n.json](https://github.com/JoseDeFreitas/wikipedia-edits-chart/blob/main/src/i18n.json)
file. To create a new translation, fork the repository and edit that file by copying the following
block right next to the name of the language you're going to translate the content to:

```json
"LANGUAGE_CODE": {
    "name": "",
    "month-names": {
        "1": "", "2": "", "3": "",
        "4": "", "5": "", "6": "",
        "7": "", "8": "", "9": "",
        "10": "", "11": "", "12": ""
    },
    "date-template": "#day #month #year",
    "text1": ["", ""],
    "text2": "",
    "text3": "",
    "text4": ["", ""],
    "text5": ["", "", ""]
},
```

Then, you just need to fill in the quotation marks with the corresponding translation. Below
is a list of remarks and examples for some of the parameters:

* `name`: The name of the language **in** that same language. Example: "日本語" instead of "Japanese".
* `month-names`: The first letter should be uppercase (just for styling reasons; the following
parameter controls that).
* `date-template`: Date order varies from country to country rather than language to language, but
there's always a more used form — that's the one you should put. Also, the program replaces
`#day`, `#month` and `#year` with the numbers and name of the month; you can customise commas, spaces,
etc. The `#month` string also accepts the first letter in uppercase (`#Month`); if you do it this way,
the month will appear in uppercase instead of lowercase (it does not depend on how you write the names
of the months in the translation file). Example: "#year#month#day" (common Japanese representation).
* `text1`: As these two strings make up a whole sentence instead of appearing separately, this may
cause some issues in some languages. If that's the case, please [open an issue](https://github.com/JoseDeFreitas/wikipedia-edits-chart/issues/new).
