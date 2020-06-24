import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import random
import pytz
from nanoid import generate
import json


# start and end date of treatment plan- dates are passed as datetime objects, ie date(2008, 8, 15)
# expectedTimes is an array of times that the medicine should be administered in a given day, in minutes
# adherence is a decimal between 0 and 1 (ie 50% adherence is passed as 0.5)
# distance is the range of how close the patient could take the medicine compared to the expected time; i.e. distance of 20 means medicine is taken 20 minutes within expected time

# returns two outputs: a dataframe and a json structure

def generatePatient(startDate, endDate, expectedTimes, adherence, distance, ndcNumber):
    # generate all dates in given interval
    days = []
    delta = endDate - startDate

    for i in range(delta.days + 1):
        day = startDate + timedelta(days=i)
        days.append(day)

    # create a dictionary for each dosage and append to patient's profile

    profile = []
    tz = pytz.timezone("US/Pacific")
    packageID = generate(size=28)

    expectedTimes.sort()  # unnecessary if input array is always sorted

    for day in days:
        for hour in expectedTimes:
            dosage = {}
            expectedTime = datetime(day.year, day.month, day.day, int(hour / 60), int(hour % 60))
            timeDiff = random.randint(-distance, distance)
            actualTime = expectedTime - timedelta(minutes=timeDiff)

            dosage['expectedTime'] = (tz.localize(expectedTime)).isoformat()

            dosage['takenAt'] = (
                np.random.choice(a=[str((tz.localize(actualTime)).isoformat()), "null"], size=1, replace=False,
                                 p=[adherence, 1 - adherence]))[0]

            dosage['packageID'] = packageID

            dosage['id'] = generate(size=28)

            dosage['ndcNumber'] = ndcNumber

            profile.append(dosage)

    return pd.DataFrame(profile), pd.DataFrame(profile).to_json(orient="records")


# sample usage
def main():
    df, j_son = generatePatient(date(2008, 8, 15), date(2008, 8, 20), [420, 1080], 0.6, 20, "hello")
    print(df)
    print()
    print(j_son)


if __name__ == "__main__":
    main()
