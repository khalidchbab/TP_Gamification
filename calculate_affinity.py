import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


PVAL = 0.1
STUDENT = ["elevebf01","eleveag02","eleveag08","elevelg11"]
PROFILE = ["achiever","player","socialiser","freeSpirit","disruptor","philanthropist"]
MOTIV = ["MI","ME","amotI"]
GameElements = ["avatar","badges","progress","ranking","score","timer"]


def get_hexad(e,p):
    df_coef = pd.read_csv("./data/Hexad/"+ e +"PathCoefs.csv",sep=";",header=0,index_col=0)
    df_pval = pd.read_csv("./data/Hexad/"+ e +"pVals.csv",sep=";",header=0,index_col=0)
    for i in range(df_coef.shape[0]):
        for j in range(df_coef.shape[1]):
            if df_pval.iloc[i,j] >= p: 
                df_pval.iloc[i,j] = np.float64()        
    return df_coef

def get_motivation(e,p):
    df_coef = pd.read_csv("./data/Motivation/"+ e +"PathCoefs.csv",sep=";",header=0,index_col=0)
    df_pval = pd.read_csv("./data/Motivation/"+ e +"pVals.csv",sep=";",header=0,index_col=0)
    for i in range(df_coef.shape[0]):
        for j in range(df_coef.shape[1]):
            if df_pval.iloc[i,j] >= p: 
                df_pval.iloc[i,j] = np.float64()        
    return df_coef

def calculate(v_aff:pd.DataFrame):
    v_aff = v_aff.squeeze()
    return v_aff.iloc[0] + v_aff.iloc[1] - v_aff.iloc[2] 

def main(ID,p):
    hexads = {}
    motivations = {}

    userStats = pd.read_csv("./data/user_stats/userStats.csv",sep=";")
    student = userStats.loc[userStats["User"] == ID]
    student["MI"],student["ME"],student["amotI"] = student[["micoI"," miacI"," mistI"]].sum(axis=1), student[[" meidI"," meinI"," mereI"]].sum(axis=1) ,  student[" amotI"]
    
    student = student[PROFILE+MOTIV]
    for e in GameElements:
        hexads[e] = get_hexad(e,p).dot(student[PROFILE].T)
        motivations[e] = get_motivation(e,p).dot(student[MOTIV].T)
        hexads[e],motivations[e] = calculate(hexads[e]),calculate(motivations[e])

    hexads = {key: value for key, value in sorted(hexads.items(), key=lambda item: -item[1])}   
    motivations = {key: value for key, value in sorted(motivations.items(), key=lambda item: -item[1])}
    
    return hexads, motivations

if __name__ == "__main__":
    print("===================================")
    print("\tKhalid CHBAB M2 IA")
    print("===================================")
    hexads,motivations = main(STUDENT[1],PVAL)
    print("Pour l'etudiant ",STUDENT[1],":\n(Hexad)")
    for k,v in hexads.items():
        print("\t",k,v)
    print("(Motivation)")
    for k,v in motivations.items():
        print("\t",k,v)
