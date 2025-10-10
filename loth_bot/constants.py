from datetime import time
from datetime import timedelta

MATINS_AND_LAUDS_DEADLINE = time(12, 0)
DAYTIME_DEADLINE = time(18, 0)
VESPERS_DEADLINE = time(22, 0)
COMPLINE_DEADLINE = time(23, 59)

REMINDER_TIMEDELTA = timedelta(minutes=-30)
