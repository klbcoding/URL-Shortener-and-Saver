from validators.url import url
import pyshorteners
import sys
from cs50 import SQL
from tabulate import tabulate

#initialize libraries
db = SQL("sqlite:///url.db")
s = pyshorteners.Shortener()

def main():
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments. Usage:: project.py [(s)horten / (e)xpand / show]")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments. Usage:: project.py [(s)horten / (e)xpand / show]")
    elif sys.argv[1].lower() not in ("s", "e", "show"):
        sys.exit("Usage:: project.py [(s)horten / (e)xpand / show]")

    #handling command-line arguments
    if sys.argv[1].lower() == "show":
        print(display_table())
        while True:
            query = input("Press 'd' to delete fields, 'e' to exit: ")
            if query.lower() in ("d", "e"):
                break
            else:
                print("Invalid input")
        if query.lower() == "e":
            sys.exit()
        elif query.lower() == "d":
            while True:
                try:
                    delete_id = int(input("Enter the id of the url to delete: "))
                except ValueError:
                    print("Must be a positive integer")
                    continue
                if db.execute("SELECT * FROM url WHERE id = ?", delete_id):
                    break
                else:
                    print("id not in database.")

            #after checking for valid inputs, delete the values associated with the id
            db.execute("DELETE FROM url WHERE id = ?", delete_id)
            print("URL deleted.")

    elif sys.argv[1].lower() == "s":
        input_url = url_checker(input("Enter URL: "))
        short_url = shorten(input_url)
        print(f"Shortened URL: {short_url}")

        #allow user to add their newly shortened URL into a database
        while True:
            save_query = input("Add URL to database? y/n: ")
            if save_query.lower() == "n":
                sys.exit()
            elif save_query.lower() == "y":
                name = input("Name of your shortened link: ")
                db.execute("INSERT INTO url (name, shortened_url) VALUES (?, ?)", name, short_url)
                sys.exit("URL added.")

    elif sys.argv[1].lower() == "e":
        print(display_table())
        while True:
            try:
                expand_id = int(input("Enter the id of the url to expand: "))
            except ValueError:
                print("Must be a positive integer.")
                continue
            if db.execute("SELECT shortened_url FROM url WHERE id = ?", expand_id):
                break
            else:
                print("id not in database.")

        #after checking for valid inputs, extract the shortened URL and return the expanded version
        input_url = db.execute("SELECT shortened_url FROM url WHERE id = ?", expand_id)[0]["shortened_url"]
        expand_url = expand(input_url)
        print(f"Expanded URL: {expand_url}")


def url_checker(s):
    if not url(s):
        sys.exit("Invalid URL.")
    return s


def shorten(url):
    try:
        return s.tinyurl.short(url)
    except pyshorteners.exceptions.ShorteningErrorException:
        sys.exit("Error when shortening URL")


def expand(url):
    try:
        return s.tinyurl.expand(url)
    except pyshorteners.exceptions.ExpandingErrorException:
        sys.exit("Error when expanding URL")


def display_table():
    url_list = db.execute("SELECT * FROM url")
    table = []
    for url_dict in url_list:
        table.append([url_dict["id"], url_dict["name"], url_dict["shortened_url"], url_dict["TIMESTAMP"]])
    return tabulate(table, headers=["id", "Name", "Shortened URL", "Timestamp"], tablefmt="grid")


if __name__ == "__main__":
    main()
