import gca_requests as gl
import secret

dict_birthdays = {
    "Rudolf Clausius": "1892-01-02",
    "Stephen Hawking": "1942-01-08",
    "Edward Teller": "1942-01-15",
    "Issac Newton": "1942-01-04",
    "Galileo Galilei": "1564-02-15",
    "Alessandro Volta": "1745-02-18",
    "Ernst Mach": "1838-02-18",
    "Linus Pauling": "1901-02-28",
    "Albert Einstein": "1745-03-14",
    "Gabriele Veneziano": "1838-03-20",
    "Leonhard Euler": "1707-04-15",
    "J. Robert Oppenheimer": "1904-04-22",
    "Max Planck": "1858-04-23",
    "Willem de Sitter": "1872-05-06",
    "Vance Brand": "1931-05-09",
    "Gaspard Monge": "1746-05-10",
    "Augustin-Jean Fresnel": "1788-05-10",
    "Lisa Nowak": "1963-05-10",
    "Richard Feynman": "1918-05-11",
    "Gabriel Fahrenheit": "1686-05-14",
    "Andrei Sakharov": "1921-05-21",
    "Rabindranath Tagore": "1861-05-07",
    "Geminiano Montanari": "1633-06-01",
    "Nicolas Léonard Sadi": "1796-06-01",
    "Edward Charles Titchmarsh": "1899-06-01",
    "Frank Whittle": "1907-06-01",
    "William S.": "1917-06-01",
    "Kip Thorne": "1940-06-01",
    "Pete Conrad,": "1930-06-02",
    "Heather Couper": "1949-06-02",
    "David Gregory": "1659-06-03",
    "Igor Shafarevich": "1923-06-03",
    "Benjamin Huntsman": "1704-06-04",
    "Heinrich Wieland": "1877-06-04",
    "Robert F.": "1916-06-04",
    "Robert Shane Kimbrough": "1967-06-04",
    "Johan Gadolin": "1760-06-05",
    "John Couch Adams": "1819-06-05",
    "Allvar Gullstrand": "1862-06-05",
    "Dennis Gabor": "1900-06-05",
    "Michael E.": "1965-06-05",
    "James Clerk Maxwell": "1831-06-13",
    "John Tyndall": "1820-08-02",
    "Ernest Rutherford": "1871-08-30",
    "Erwin Schrödinger": "1887-08-12",
    "Paul Dirac": "1902-08-08",
    "Valery Bykovsky": "1934-08-02",
    "Edward Witten": "1951-08-08",
    "Koichi Tanaka": "1959-08-03",
    "Michael Faraday": "1791-09-22",
    "Enrico Fermi": "1901-09-29",
    "Chen Ning Yang": "1922-10-01",
    "Niels Bohr": "1885-10-07",
    "Carl Sagan": "1934-11-09",
    "Lisa Meitner": "1878-11-07",
    "Marie Curie": "1867-11-07",
    "Dmitri Skobeltsyn": "1892-11-24"}

if __name__ == "__main__":
    #Checking
    list_calendar = gl.retrieve_list_calendars()["items"]
    events = gl.retrieve_calendar_events_by_id(secret.CALENDAR_ID)

    #Birthdays
    for key, value in dict_birthdays.items():
        gl.create_event("date", secret.CALENDAR_ID, "2019"+value[4:], key, 24, description=value, recurrence="YEARLY")

    # #delete events
    # gl.delete_events(secret.CALENDAR_ID, events)