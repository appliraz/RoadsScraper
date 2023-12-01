import requests
from bs4 import BeautifulSoup

EVENT_ROADNAME = 'roadNumber'
EVENT_DESCRIPTION = 'description'
EVENT_TYPE = 'roadConstruction'
EVENT_CLASS = 'reportsList__item'
RELEVANT_ROAD_NAMES = ["כביש 1", "כביש 4", "כביש 44"]
SCRAP_URL = 'https://www.iroads.co.il/#roadConstruction'



def getUrl():
    return SCRAP_URL

def getSoup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def getRoadName(event):
    interesting_roads = RELEVANT_ROAD_NAMES # to narrow all the updates only to relevant roads names
    try:
        road = event.find(class_=EVENT_ROADNAME).get_text().strip()
    except Exception as e:
        print(e)
        return None
    for interesting in interesting_roads:
        if road == interesting:
            return road
    return None

def getDescription(event):
    try:
        description = event.find(class_=EVENT_DESCRIPTION).get_text().strip()
        description = description.replace("\n", " ").replace("\r", "").replace("\t", "") # cleanup
    except Exception as e:
        print(e)
        return None
    return description

def getScrapedEvent(event):
    road = getRoadName(event)
    if road is None:
        return None
    description = getDescription(event)
    if description is None:
        return None
    return (road, description)

def getScrapedEvents(soup_events):
    scraped_events = []
    for event in soup_events:
        scraped_event = getScrapedEvent(event)
        if scraped_event is None:
            continue
        scraped_events.append(scraped_event)
    return scraped_events

def getEventsFromSoup(soup):
    scrap_type_id = EVENT_TYPE
    event_class = EVENT_CLASS
    roads_div = soup.find("div", {"id": scrap_type_id})
    events = roads_div.find_all(class_ = event_class )
    scraped_events = getScrapedEvents(events)
    return scraped_events

def scrap_israel_roads():
    url = getUrl()
    soup = getSoup(url)
    events = getEventsFromSoup(soup)
    if not events:
        title = "No Working On The Roads Today at Nativay Israel"
        description = "Could not find any expected plans to work on the roads. Drive safe!"
        return [(title, description)]
    return events


if __name__=="__main__":
    scrap_israel_roads()
