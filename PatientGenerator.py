import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import random
import json

#start and end date of treatment plan- dates are passed as datetime objects, ie date(2008, 8, 15)
#frequency is how many times per day the medicine should be taken
#adherence is a decimal between 0 or 1 (ie 50% adherence is passed as 0.5)
#distance is the range of how close the patient can take the medicine compared to the expected time; i.e. distance of 20 means medicine is taken 20 minutes within expected time

#returns two outputs: a dataframe and a json structure

def generatePatient(start, end, frequency, adherence, distance):


    # generate all dates in given interval
    days = []
    delta = end - start

    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        days.append(day)


    # randomly generate the hours that the medicine should be administered each day, between 10am and 8pm
    hours = range(10, 20)

    expectedTimes = random.sample(hours, frequency)
    expectedTimes.sort()


    # create a dictionary for each dosage and append to patient's profile

    profile = []

    for day in days:
        for hour in expectedTimes:
            dosage = {}
            expectedTime = datetime(day.year, day.month, day.day, hour)
            timeDiff = random.randint(-distance, distance)
            actualTime = expectedTime - timedelta(minutes=timeDiff)

            dosage['Expected Time'] = str(expectedTime.isoformat())

            dosage['Actual Time'] = np.random.choice(a=[str(actualTime.isoformat()), "null"], size=1, replace=False, p=[adherence, 1 - adherence])

            profile.append(dosage)

    return pd.DataFrame(profile), pd.DataFrame(profile).to_json()

#sample usage
def main():
    df, j_son= generatePatient(date(2008, 8, 15), date(2008, 8, 20), 2, 0.6, 20)
    print(df)
    print()
    print(j_son)





if __name__ == "__main__":
    main()