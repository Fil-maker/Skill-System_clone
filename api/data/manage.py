import json

import requests
from bs4 import BeautifulSoup
from flask_migrate import MigrateCommand
from flask_script import Manager

from api import app
from api.data.db_session import create_session
from api.data.models.country import Country
from api.data.models.region import Region

manager = Manager(app)
manager.add_command("db", MigrateCommand)


@manager.command
def initialize_db():
    """Fills the database with initial data (list of countries and regions of Russia)"""
    fill_countries()
    fill_regions()


def fill_countries():
    countries = get_countries()
    with create_session() as session:
        for country in countries:
            session.add(Country(name=country["name"],
                                alpha_code=country["alpha_code"],
                                numeric_code=country["numeric_code"]))
    print(f"Successfully added {len(countries)} countries")


def fill_regions():
    regions = get_regions()
    with create_session() as session:
        ru_id = session.query(Country).filter(Country.name.like("%Russian Federation%")).first().id
        for region in regions:
            session.add(Region(name=region["name"],
                               code=region["code"],
                               country_id=ru_id))
    print(f"Successfully added {len(regions)} regions")


def get_countries():
    with open("api/data/initialization.json") as file:
        data = json.load(file)
        return data["countries"]


def get_regions():
    with open("api/data/initialization.json") as file:
        data = json.load(file)
        return data["regions"]


def parse_wiki_country_list():
    try:
        url = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
        page = requests.get(url)
    except ConnectionError:
        print("Network error")
        return exit(0)
    soup = BeautifulSoup(page.text, "lxml")
    data = []
    tbody = soup.select_one("#mw-content-text > div.mw-parser-output > table > tbody")
    # If the page has been changed, the selector may not work. Check it with browser developer tools
    for tr in tbody.select("tr"):
        td = tr.select("td")
        if len(td) < 6:
            continue
        name = td[0].select_one("a:not(span a)").text.strip()
        alpha_code = td[3].text.strip()
        num_code = td[5].text.strip()
        data.append({
            "name": name,
            "alpha_code": alpha_code,
            "numeric_code": num_code
        })
    return data


def parse_wiki_region_list():
    try:
        url = "https://en.wikipedia.org/wiki/Federal_subjects_of_Russia"
        page = requests.get(url)
    except ConnectionError:
        print("Network error")
        return exit(0)
    soup = BeautifulSoup(page.text, "lxml")
    data = []
    tbody = soup.select("table.wikitable.sortable > tbody")[2]
    # If the page has been changed, the selector may not work. Check it with browser developer tools
    for tr in tbody.select("tr"):
        td = tr.select("td")
        if len(td) < 2:
            continue
        code = td[0].text.strip()
        name = td[1].a.text.strip()
        data.append({
            "name": name,
            "code": code
        })
    return data


if __name__ == "__main__":
    manager.run()
