from bs4 import BeautifulSoup
import requests
import dateparser

EVENTS_SECTION = 'events__group'
EVENTS_TODAY_SECTION = 'events__group__items'
EVENT_ELEMENT = 'event'
EVENT_TITLE_TAG = 'h4'
EVENT_DESCRIPTION_TAG = 'p'
SCRAP_URL = "https://www.ayalonhw.co.il/events/"

def getEvents(soup):
    events = soup.find_all(class_=EVENTS_SECTION)
    today = dateparser.getTodayAsDayOfTheWeek()
    if today is None or not events:
        return None
    print(f"today = {today}")
    events_today_soup = events[today].find(class_=EVENTS_TODAY_SECTION).find_all(class_=EVENT_ELEMENT)
    if not events_today_soup:
        title = "No Working On The Roads Today at Ayalon"
        description = "Could not find any expected plans to work on the roads. Drive safe!"
        return [(title, description)]
    events_today_list = []
    i = 0
    for event in events_today_soup:
        print(i)
        i+=1
        print(event)
        try:
            title = event.find(EVENT_TITLE_TAG).get_text()
            description = event.find_all(EVENT_DESCRIPTION_TAG)[1].get_text()
            events_today_list.append((title, description))
        except Exception as e:
            print("Error in getEvents")
            print(e)
            print(event)
            continue
    return events_today_list


def scrap_ayalon_roads():
    ayalon_web = SCRAP_URL
    r = requests.get(ayalon_web)
    if r.status_code == 404:
        return ['no valid url to ayalon roads, 404 received', f'cannot scrap from {ayalon_web}']
    soup = BeautifulSoup(r.text, "html.parser")
    events = getEvents(soup)
    print(events)
    return events


if __name__ == "__main__":
    scrap_ayalon_roads()