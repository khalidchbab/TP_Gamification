import pandas as pd
import numpy as np
from algorithm import algo
from datetime import datetime

INFOS = ["Time","CorrectCount","FullyCompletedLessonCount","MiVar","MeVar"," amotVar"]
EPSILON = 0.1

def to_second(date):
    dt = datetime.strptime(date, "%H:%M:%S")
    return (dt.hour * 3600) + (dt.minute * 60) + dt.second 

def evaluate():
    userStats = pd.read_csv("./data/user_stats/userStats.csv",sep=";")
    userStats["Time"] = userStats["Time"].apply(to_second) # On converti le temps en seconde 
    userStats["MiVar"] = userStats[[" micoVar", " miacVar", " mistVar"]].sum(axis=1)
    userStats["MeVar"] = userStats[[" meidVar", " meinVar", " mereVar"]].sum(axis=1)

    students = userStats["User"]
    recommendations = []
    print("Nombre des etudiant : ", len(students))
    for student in students:
        recommendations.append(algo(student,EPSILON))
    userStats["Recomendation"] = recommendations
    userStats["Adapted"] = userStats["Recomendation"] == userStats["GameElement"]
    groupeAdapted = userStats.loc[userStats["Adapted"]]
    groupeNotAdapted = userStats.loc[userStats["Adapted"] == False]

    print(f"Nombre de recommendations correspondantes {groupeAdapted.shape[0]}/{len(students)}")
    print(f"Nombre de recommendations différente {groupeNotAdapted.shape[0]}/{len(students)}")
    
    print(userStats.Recomendation.value_counts())
    print("=================================== \n \t Info \n===================================")
    print(userStats[INFOS].describe())

if __name__ == "__main__":
    print("===================================")
    print("\tKhalid CHBAB M2 IA")
    print("===================================")

    evaluate()
