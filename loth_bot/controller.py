from typing import Iterable

from .models import Hour
from .models import Requirement

matins_prayed = False
lauds_prayed = False
daytime_prayed = False
vespers_prayed = False
compline_prayed = False

hours_missed = 0


def pray_hour(hour: Hour) -> None:
    global matins_prayed
    global lauds_prayed
    global daytime_prayed
    global vespers_prayed
    global compline_prayed

    if hour == Hour.MATINS:
        matins_prayed = True
        return
    if hour == Hour.LAUDS:
        lauds_prayed = True
        return
    if hour in (Hour.TERCE, Hour.SEXT, Hour.NONE):
        daytime_prayed = True
        return
    if hour == Hour.VESPERS:
        vespers_prayed = True
        return
    if hour == Hour.COMPLINE:
        compline_prayed = True
        return


def check_requirements(
    requirements: Iterable[Requirement], increment_missed: bool = True
) -> list[Requirement]:
    global matins_prayed
    global lauds_prayed
    global daytime_prayed
    global vespers_prayed
    global compline_prayed

    global hours_missed

    requirement_lookup = {
        Requirement.MATINS: matins_prayed,
        Requirement.LAUDS: lauds_prayed,
        Requirement.DAYTIME: daytime_prayed,
        Requirement.VESPERS: vespers_prayed,
        Requirement.COMPLINE: compline_prayed,
    }
    missed_requirements = [r for r in requirements if not requirement_lookup[r]]
    if increment_missed:
        hours_missed += len(missed_requirements)
    return missed_requirements


def reset_prayed() -> None:
    global matins_prayed
    global lauds_prayed
    global daytime_prayed
    global vespers_prayed
    global compline_prayed

    matins_prayed = False
    lauds_prayed = False
    daytime_prayed = False
    vespers_prayed = False
    compline_prayed = False


def reset_missed_hours() -> None:
    global hours_missed

    hours_missed = 0


def get_hours_missed() -> int:
    global hours_missed

    return hours_missed
