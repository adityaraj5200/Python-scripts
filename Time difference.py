from datetime import date
from dateutil.relativedelta import relativedelta

# ----------------------------
# PLACEHOLDER VARIABLES
# ----------------------------

START_DAY   = 15
START_MONTH = 3
START_YEAR  = 2025

# Toggle this flag 👇
USE_TODAY_AS_END_DATE = True

# Only used if USE_TODAY_AS_END_DATE = False
END_DAY     = 1
END_MONTH   = 12
END_YEAR    = 2025

# ----------------------------
# CREATE DATE OBJECTS
# ----------------------------

start_date = date(START_YEAR, START_MONTH, START_DAY)

if USE_TODAY_AS_END_DATE:
    end_date = date.today()
else:
    end_date = date(END_YEAR, END_MONTH, END_DAY)

# Ensure correct order
if end_date < start_date:
    start_date, end_date = end_date, start_date

# ----------------------------
# DATE DIFFERENCE
# ----------------------------

delta = relativedelta(end_date, start_date)
total_days = (end_date - start_date).days

# ----------------------------
# OUTPUT
# ----------------------------

print("Date Difference")
print("----------------")
print(f"Years  : {delta.years}")
print(f"Months : {delta.months}")
print(f"Days   : {delta.days}")
print(f"Total Days : {total_days}")
print(f"End Date Used : {end_date}")
