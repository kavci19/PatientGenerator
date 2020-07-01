from nanoid import generate
import numpy as np
import matplotlib.pyplot as plt
import dateutil.parser
from datetime import date
import matplotlib.ticker as plticker

size = 12

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
    return 1 + 2 * np.log10(day / 7)


# plots the expected time of dosage vs actual time of dosage over treatment plan
def plotAdherence(days, expectedTimes, actualTimes, originalTimes, ticks, adherence, caption):
    # scale adherence rate to y axis range
    adherence = [1440 * i for i in adherence]
    ax = plt.gca()

    plt.scatter(days, expectedTimes, alpha=0.5, c='grey', label='Expected', s=10)
    plt.scatter(days, actualTimes, alpha=0.5, c='blue', label='Actual')
    plt.scatter([], [], alpha=0.5, c='red', label='Missed', marker='X')

    # plot missed dosages as X
    for i in range(len(actualTimes)):
        if actualTimes[i] is None:
            hours = originalTimes[i].hour * 60 + originalTimes[i].minute
            ax.plot(days[i], hours, marker='x', linestyle='', ms=6, c='red')

    plt.legend()
    plt.title('Expected vs Actual Doses Over Time')
    plt.xlabel('Date')
    plt.ylabel('Hour')
    ax.tick_params(axis='x', which='major', labelsize=8)
    plt.gcf().autofmt_xdate()
    ax.xaxis.set_major_locator(ticks)
    ax.set_ylim([0, 1440])
    plt.yticks(ticks=[120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440])
    labels = ['2:00', '4:00', '6:00', '8:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '24:00']
    ax.set_yticklabels(labels)
    # plt.fill_between(days, adherence, color="skyblue", alpha=0.2, step='mid')
    plt.fill_between(days, adherence, color="skyblue", alpha=0.2, step='mid')

    ax2 = plt.twinx()
    ax2.set_ylabel('Adherence Rate')
    ax2.set_yticklabels(
        ['0.0', '0.2', '0.4', '0.6', '0.8', '1.0'])

    plt.figtext(0.5, 0.01, caption, ha="center", fontsize=size,
                bbox={"facecolor": "purple", "alpha": 0, "pad": 20})

    plt.show()


# determine the frequency of x ticks in a given time range
def calculateXTicks(startAt, endAt):
    delta = (endAt - startAt).days

    x = int(delta / 10)

    ticks = plticker.MultipleLocator(base=x)

    return ticks


# extract coordinates from dataframe object for plotting
def generateCoordinates(df):
    dates = []
    actualTimes = []
    expectedTimes = []
    originalTimes = [dateutil.parser.parse(i) for i in df['expectedAt'].to_list()]

    for i in range(len(df['expectedAt'].to_list())):
        # if dose was missed, delete the dose from actual and expected lists and let the originalTimes plot it
        if df['takenAt'].to_list()[i] is None:
            actualTimes.append(None)
            expectedTimes.append(None)
        else:
            aDT = dateutil.parser.parse(df['takenAt'].to_list()[i])
            actualTimes.append(aDT.hour * 60 + aDT.minute)
            eDT = dateutil.parser.parse(df['expectedAt'].to_list()[i])
            expectedTimes.append(eDT.hour * 60 + eDT.minute)
        ndate = originalTimes[i]
        dates.append(date(ndate.year, ndate.month, ndate.day))

    return expectedTimes, actualTimes, dates, originalTimes


def createCaption(dosageEvents, adjustmentsList):
    num = 1
    output = ''
    adjustStr = ''
    ct=1
    global size

    for i in adjustmentsList:
        adjustStr += str(i) + ', '
    lci = len(adjustStr)-2
    adjustStr = adjustStr[:lci] + adjustStr[lci+1:]



    for dose in dosageEvents:
        ct += 1
        hour = int(dose.expectedTime / 60)
        ampm = ''
        if hour > 12:
            ampm = 'PM'
            hour = hour - 12
        else:
            ampm = 'AM'

        output += 'Dose ' + str(num) + ' at ' + str(hour) + ampm + ' +/- ' + str(dose.distance) + ' minutes @ ' + str(
            dose.adherence) + '% base adherence' + '\n' + '\n'


        if (ct%4 == 0):
            size = size *0.6

    print(ct)
    output += 'For days Monday - Sunday, adherence increases by the following ratios: ' + adjustStr

    return output
