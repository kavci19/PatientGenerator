from nanoid import generate


def generateNDC():
    dash = '-'
    id1 = generate('1234567890', 4)
    id2 = generate('1234567890', 4)
    id3 = generate('1234567890', 2)
    return id1 + dash + id2 + dash + id3

#sample adherenceTrend growth function where adherence grows by 10% each day
def linearGrowth(day=0):
    return 1 + 0.1*day