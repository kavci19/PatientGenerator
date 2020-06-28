from datetime import date
from dosageEvent import DosageEvent
from suppFunctions import linearGrowth
from patientGenerator import generatePatient

# sample usage

def main():
    df, json = generatePatient(
        # 5 days
        startAt=date(2020, 1, 15),
        endAt=date(2020, 1, 19),
        # a drug
        ndcNumber="0101-0155-10",
        # morning and evening dose
        dosageEvents=[
            # 7 AM, 75% adherence, within 20 minutes
            DosageEvent(420, 0.75, 20),
            # 6 PM, 50% adherence, within 60 minutes
            DosageEvent(1080, 0.5, 20)
        ],
        # adherence that is above average during the week
        # and below average on the weekend
        weeklyAdherence=[0, 0.25, 0.25, 0.5, 0.25, -0.5, -0.5],
        # adherence improving daily
        adherenceTrend=linearGrowth)

    print(df)
    print()
    print(json)


if __name__ == "__main__":
    main()
