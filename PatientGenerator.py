import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import random
import pytz
from nanoid import generate

# start and end date of treatment plan - dates are passed as datetime objects, ie date(2008, 8, 15)
# expectedTimes is an array of times that the medicine should be administered in a given day, in minutes
# adherenceRate is a decimal between 0 and 1 (ie 50% adherenceRate is passed as 0.5)
# distance is the range of how close the patient could take the medicine compared to the expected time; i.e. distance of 20 means medicine is taken 20 minutes within expected time

# returns two outputs: a dataframe and a json structure

def generatePatient(startAt, endAt, expectedTimes, adherenceRate, distance, ndcNumber):
    # generate all dates in given interval
    days = []
    delta = endAt - startAt

    for i in range(delta.days + 1):
        day = startAt + timedelta(days=i)
        days.append(day)

    # create a dictionary for each dosage and append to patient's profile

    profile = []
    tz = pytz.timezone("US/Eastern")
    packageId = generate(size=28)

    expectedTimes.sort()  # unnecessary if input array is always sorted

    for day in days:
        for hour in expectedTimes:
            expectedAt = datetime(day.year, day.month, day.day, int(hour / 60), int(hour % 60))
            timeDiff = random.randint(-distance, distance)
            actualAt = expectedAt - timedelta(minutes=timeDiff)

            dose = {
                "id": generate(size=28),
                "packageId": packageId,
                "ndcNumber": ndcNumber,
                "expectedAt": (tz.localize(expectedAt)).isoformat(),
                "takenAt": np.random.choice(
                    a=[str((tz.localize(actualAt)).isoformat()), None],
                    size=1,
                    replace=False,
                    p=[adherenceRate, 1 - adherenceRate]
                )[0]
            }
            profile.append(dose)

    return pd.DataFrame(profile), pd.DataFrame(profile).to_json(orient="records")


# sample usage
def main():
    df, json = generatePatient(date(2020, 1, 15), date(2020, 1, 20), [420, 1080], 0.6, 20, "0071-0155-10")
    print(df)
    print()
    print(json)


if __name__ == "__main__":
    main()
