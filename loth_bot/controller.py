from .models import Hour

matins_prayed = False
lauds_prayed = False
midday_prayed = False
vespers_prayed = False
compline_prayed = False


def pray_hour(hour: Hour) -> None:
    global matins_prayed
    global lauds_prayed
    global midday_prayed
    global vespers_prayed
    global compline_prayed

    if hour == Hour.MATINS:
        matins_prayed = True
        return
    if hour == Hour.LAUDS:
        lauds_prayed = True
        return
    if hour in (Hour.TERCE, Hour.SEXT, Hour.NONE):
        midday_prayed = True
        return
    if hour == Hour.VESPERS:
        vespers_prayed = True
        return
    if hour == Hour.COMPLINE:
        compline_prayed = True
        return
