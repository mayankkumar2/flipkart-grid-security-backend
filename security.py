import requests
import bs4


def find_vulneribilites(repo):
    r = requests.get(f"https://snyk.io/test/github/{repo}")
    if r.status_code != 200:
        raise Exception("not 200 status code!")
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    divs = soup.find_all("div", class_="issue")
    alerts = {
        "critical": [],
        "high": [],
        "medium": [],
        "low": []
    }
    for i in divs:
        label = i.find("span", class_="label__text").get_text().strip()
        heading = i.find("h3", class_="heading__title").get_text().strip()
        for k in alerts:
            if k in label.lower():
                alerts[k].append(heading)
    return alerts
