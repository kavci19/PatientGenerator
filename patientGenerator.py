import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import random
import pytz
from nanoid import generate
from dosageEvent import DosageEvent
from suppFunctions import generateNDC


# startAt and endAt is the time range of treatment plan - dates are passed as datetime objects, ie date(2008, 8, 15)

# dosageEvents is an array of DosageEvent objects. A DosageEvent object contains the properties expectedTime
# (expected time of administering, in mins), adherence (decimal between 0 and 1), and distance (range of how close
# the patient could take the medicine compared to the expected time)

# weeklyAdherence is an array of 7 numbers (corresponding to each day of the week) that adjusts base adherence by a given percentage; index 0 is Monday

# adherenceTrend is a function that takes in the day as a parameter and adjusts daily adherence

# returns two outputs: a dataframe and a json structure representing the generated patient profile

def generatePatient(
        patientId=generate(size=28),
        caregiverId=generate(size=28),
        startAt=date(2020, 1, 1),
        endAt=date(2020, 2, 1),
        ndcNumber=generateNDC(),
        dosageEvents=[DosageEvent(480, 0.5, 60)],
        weeklyAdherence=[0] * 7,
        adherenceTrend=None):
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
    dayIndex = 1

    for day in days:
        for dosageEvent in dosageEvents:
            expectedAt = datetime(
                day.year,
                day.month,
                day.day,
                int(dosageEvent.expectedTime / 60),
                int(dosageEvent.expectedTime % 60))

            timeDiff = random.randint(-dosageEvent.distance, dosageEvent.distance)
            actualAt = expectedAt - timedelta(minutes=timeDiff)

            # modify adherence based on day of the week and adherenceTrend
            dayOfWeek = expectedAt.weekday()
            adherenceToday = dosageEvent.adherence * (1 + weeklyAdherence[dayOfWeek])
            if adherenceTrend is not None:
                adherenceToday = adherenceToday * adherenceTrend(dayIndex)

            # if adherenceToday or 1-adherenceToday becomes negative, need to avoid negative probability
            if adherenceToday > 1:
                adherenceToday = 1
            if adherenceToday < 0:
                adherenceToday = 0

            takenAt = np.random.choice(
                a=[actualAt, None],
                size=1,
                replace=False,
                p=[adherenceToday, 1 - adherenceToday]
            )[0]

            dose = {
                "id": generate(size=28),
                "packageId": packageId,
                "ndcNumber": ndcNumber,
                "patientId": patientId,
                "caregiverId": caregiverId,
                "expectedAt": (tz.localize(expectedAt)).isoformat(),
                "takenAt": (tz.localize(takenAt)).isoformat() if takenAt else None

            }
            profile.append(dose)

        dayIndex += 1

    return pd.DataFrame(profile), pd.DataFrame(profile).to_json(orient="records")
