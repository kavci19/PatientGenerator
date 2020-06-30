from nanoid import generate
import numpy as np
import matplotlib.pyplot as plt
import dateutil.parser
from datetime import date
import matplotlib.ticker as plticker



def generateNDC():
    dash = '-'
    id1 = generate('1234567890', 4)
    id2 = generate('1234567890', 4)
    id3 = generate('1234567890', 2)
    return id1 + dash + id2 + dash + id3


# adherence grows by 10% each day
def linearGrowth(day=1):
    return 1 + 0.05 * day


# adherence grows more slowly per week
def logGrowth(day=1):
    return 1 + 0.5 * np.log10(day / 7)


# plots the expected time of dosage vs actual time of dosage over treatment plan
def plotAdherence(days, expectedTimes, actualTimes):
    ax = plt.gca()

    plt.scatter(days, expectedTimes, alpha=0.5, c='red', label='Expected')
    plt.scatter(days, actualTimes, alpha=0.5, c='blue', label='Actual')
    plt.legend()
    plt.title('Expected vs Actual Doses Over Time')
    plt.xlabel('Date')
    plt.ylabel('Hour')
    ax.tick_params(axis='x', which='major', labelsize=8)
    plt.gcf().autofmt_xdate()
    loc = plticker.MultipleLocator(base=3.0)
    ax.xaxis.set_major_locator(loc)

    ax.set_ylim([0, 1440])

    plt.yticks(ticks=[120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440])
    labels = ['2:00', '4:00', '6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '24:00']
    ax.set_yticklabels(labels)

    plt.show()


# extracts coordinates from dataframe object for plotting
def generateHours(df):
    dates = []
    actualTimes = []
    expectedTimes = []

    for i in df['takenAt'].to_list():
        if i:
            aDT = dateutil.parser.parse(i)
            a = aDT.hour * 60 + aDT.minute

        else:
            a = None
        actualTimes.append(a)

    for i in df['expectedAt'].to_list():
        eDT = dateutil.parser.parse(i)
        dates.append(date(eDT.year, eDT.month, eDT.day))
        expectedTimes.append(eDT.hour * 60 + eDT.minute)

    return expectedTimes, actualTimes, dates
