from nativay import scrap_israel_roads
from ayalon import scrap_ayalon_roads
from emailSender import handle404, sendEmailsToReceivers

def main():
    try:
        ayalon_events = scrap_ayalon_roads()
        nativay_events = scrap_israel_roads()
        if ayalon_events is None or nativay_events is None:
            handle404()
            return
        events = ayalon_events + nativay_events
        sendEmailsToReceivers(events)
        print("finished sending emails")
    except Exception as e:
        print(e)
        handle404()


if __name__ == "__main__":
    main()