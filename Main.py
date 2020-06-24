from datetime import date
from dosageEvent import DosageEvent
from suppFunctions import linearGrowth
from PatientGenerator import generatePatient


#sample usage

def main():
    dosage1 = DosageEvent(420, 0.5, 20)
    dosage2 = DosageEvent(1080, 0.5, 20)

    df, json = generatePatient(
        date(2020, 1, 15),
        date(2020, 1, 20),
        "0101-0155-10",
        "0061-0155-10",
        "0071-0155-10",
        [0, 0.25, 0.25, 0.5, 0.25, -0.5, -0.5],
        [dosage1, dosage2],
        linearGrowth)


    print(df)
    print()
    print(json)


if __name__ == "__main__":
    main()
