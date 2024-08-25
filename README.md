# URL shortener and saver
A Python project that uses the `pyshorteners` library to shorten Uniform Resource Locators (URLs). It can also store shortened URLs into a SQL database.
### Video description
Here is a video showcasing the project: [Video here](https://youtu.be/bOgD4w0UkVY)
### Synopsis
Perhaps you may have hit the word count on a post due to a long URL, or just want to make a URL look more visually appealing for your most recent social media pitch. URLs are web addresses that allow you to visit specific webpages. However, URLs can be really long. Luckily, this software offers the ability to shorten long URLs for personal use.

### Project dependencies
1. The URL shortener utilises Tinyurl's web service, which provides aliases for URLs. The simplest usage is as shown:
```
import pyshorteners

s = pyshorteners.Shortener()
print(s.tinyurl.short('https://www.google.com/'))
```
The full documentation for `pyshorteners` is [here](https://pyshorteners.readthedocs.io/en/latest/).

2. `pytest` is also used for unit testing. It allows you to perform functional testing to ensure that your code works perfectly. Full documentation [here](https://docs.pytest.org/en/stable/).

3. The `cs50` library is used to import SQL for access to databases. The full documentation is [here](https://cs50.readthedocs.io/libraries/cs50/python/?highlight=sql).

```
from cs50 import SQL

db = SQL("sqlite:///url.db")    # initialising the database
```

4. `sys` is a built-in library in Python. `sys.argv` provides a list of command-line arguments, and `sys.exit()` allows you to exit a program with a message stated as a positional argument.

5. Lastly, we have `tabulate`, which is a library that allows you to pretty-print table data in Python.
```
from tabulate import tabulate
```

The full documentation is [here](https://pypi.org/project/tabulate/)

### project.py

This Python file contains all the code for the program. The functions used are `main()`, `url_checker(s)`, `shorten(url)`, `expand(url)` and `display_table()`.

#### main()
This function implements all the functions to run the program. Initially, `sys.argv` is used to count the number of command-line arguments used. To use the program in the terminal, type `python project.py`, followed by 1 more command-line argument `s` for shorten mode, `e` for expand mode, or `show` to show all saved URLs.
```
def main():
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments. Usage:: project.py [(s)horten / (e)xpand / show]")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments. Usage:: project.py [(s)horten / (e)xpand / show]")
    elif sys.argv[1].lower() not in ("s", "e", "show"):
        sys.exit("Usage:: project.py [(s)horten / (e)xpand / show]")
```
In `show` mode, a table made by `display_table()` will be displayed. Press `d` to delete a URL in the database, and `e` to exit. Upon pressing `d`, a prompt will request for the id of the URL to be deleted. If a non-integer or a id value not associated with any URL is passed, the program will reprompt the user.

Upon activating `s` or "shorten" mode, the user will be prompted to enter a raw URL to be shortened. The URL passes through `shorten(url)` and returns a shortened URL. Afterwards, the program will prompt again asking if the user wishes to save the URL with `y` (yes) or `n` (no). Finally, the program will allow the user to enter a name for the URL for reference.

Upon activating `e` or "expand" mode, a table made by `display_table()` will be displayed. The program will prompt the user for the id of the URL to be expanded. Afterwards, `expand(url)` returns the expanded URL. If a non-integer or a id value not associated with any URL is passed, the program will reprompt the user.

#### url_checker()
This function utilises the `validators.url` library to validate a URL. If `url(s)` is not a URL, it becomes a falsy expression as `url("not a url").__bool__()` returns False. Hence, `url_checker` can be defined as follows:
```
def url_checker(s):
    if not url(s):
        sys.exit("Invalid URL.")
    return s
```

#### shorten(url)
This function takes the URL as a parameter, and executes `s.tinyurl.short(url)`, returning a shortened URL.
```
def shorten(url):
    try:
        return s.tinyurl.short(url)
    except pyshorteners.exceptions.ShorteningErrorException:
        sys.exit("Error when shortening URL")
```

#### expand(url)
This function does the opposite. It takes the shortened URL as a parameter, and executes `s.tinyurl.expand(url)`, returning the original URL.
```
def expand(url):
    try:
        return s.tinyurl.expand(url)
    except pyshorteners.exceptions.ExpandingErrorException:
        sys.exit("Error when expanding URL")
```

#### display_table()
This function converts a list of dictionaries obtained from an SQL query into a list of lists which can then be tabulated.
```
def display_table():
    url_list = db.execute("SELECT * FROM url")
    table = []
    for url_dict in url_list:
        table.append([url_dict["id"], url_dict["name"], url_dict["shortened_url"], url_dict["TIMESTAMP"]])
    return tabulate(table, headers=["id", "Name", "Shortened URL", "Timestamp"], tablefmt="grid")
```

### test_project.py
This file contains all the unit tests using `pytest`. Multiple assert statements are passed to check for correctness.

### requirements.txt
This file contains the names of the libraries used, and their versions.

