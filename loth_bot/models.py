from enum import StrEnum


class Hour(StrEnum):
    MATINS = "matins"
    LAUDS = "lauds"
    TERCE = "terce"
    SEXT = "sext"
    NONE = "none"
    VESPERS = "vespers"
    COMPLINE = "compline"


class Requirement(StrEnum):
    MATINS = "matins"
    LAUDS = "lauds"
    DAYTIME = "daytime prayer"
    VESPERS = "vespers"
    COMPLINE = "compline"
