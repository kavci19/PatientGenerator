from dosageEvent import DosageEvent
from suppFunctions import *
from patientGenerator import generatePatient


# sample usage

def main():
    start = date(2020, 1, 15)
    end = date(2020, 5, 15)

    df, jsonP = generatePatient(
        # 2 months
        startAt = start,
        endAt = end,
        # a drug
        ndcNumber="0101-0155-10",
        # morning and evening dose
        dosageEvents=[
            # 7 AM, 40% adherence, within 100 minutes
            DosageEvent(420, 0.2, 100),

            # 6 PM, 20% adherence, within 60 minutes
            DosageEvent(1080, 0.2, 60)
        ],
        # adherence that is above average during the week
        # and below average on the weekend,
        weeklyAdherence=[0.25, 0.25, 0.25, 0.25, 0.25, -0.25, 0.25],
        # adherence improving each week, more slowly over time
        adherenceTrend=logGrowth,
        adherenceCoeff=0.4)


    expectedTimes, actualTimes, dates, originalTimes = generateCoordinates(df)
    ticks = calculateXTicks(start, end)
    caption = createCaption([DosageEvent(420, 0.2, 100), DosageEvent(900, 0.4, 50)], [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25] )
    plotAdherence(dates, expectedTimes, actualTimes, originalTimes, ticks, df['adherence'].to_list(), caption)

if __name__ == "__main__":
    main()
