from datetime import date, datetime

def addLeadingZero(num):
    if int(num)<10:
        return "0"+str(num)
    return str(num)

def getMonth():
    month = date.today().month
    return addLeadingZero(month)

def getDay():
    day = date.today().day
    return addLeadingZero(day)

def getTodayAsString():
    today = date.today()
    year = today.year
    month = getMonth()
    day = getDay()
    return f"{year}-{month}-{day}"

""" This Function is used primarly to get an event out of a list of events that is corresponding to the local day date in which the script was used"""
def getTodayAsDayOfTheWeek():
    try:
        today = datetime.now().date().strftime("%w")  # get the week day where sunday = 0
        today = int(today)
        return today
    except Exception as e:
        print(e)
        return None

