import pandas as pd
import numpy as np

injury = pd.read_csv("Injuries Databases.csv")
print(injury, sep="\n")



def c_proc():
    injuries = ["Ankle", "Back", "Calf", "COVID19", "Foot", "Groin", "Hamstring", "Head", "Knee", "Knock",
                "Muscles", "Shoulder", "Thigh", "OthCauses", "OthMembers"]

    valori = []
    for i in range(len(injury)):
        _v = []
        for (j, k) in zip(injuries, range(len(injuries))):
            f_proc = float((injury[j][i] / injury["PlayerNumbers"][i]) * 100)
            _v.append(f_proc)
        valori.append(_v)

    return np.array(valori)

p_echipe['Ankle'] = pd.to_numeric(p_echipe['Ankle']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['Back'] = pd.to_numeric(p_echipe['Back']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['Calf'] = pd.to_numeric(p_echipe['Calf']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['COVID19'] = pd.to_numeric(p_echipe['COVID19']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['Foot'] = pd.to_numeric(p_echipe['Foot']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['Groin'] = pd.to_numeric(p_echipe['Groin']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['Hamstring'] = pd.to_numeric(p_echipe['Hamstring']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['Head'] = pd.to_numeric(p_echipe['Head']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['Knee'] = pd.to_numeric(p_echipe['Knee']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['Knock'] = pd.to_numeric(p_echipe['Knock']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['Muscles'] = pd.to_numeric(p_echipe['Muscles']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['Shoulder'] = pd.to_numeric(p_echipe['Shoulder']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['Thigh'] = pd.to_numeric(p_echipe['Thigh']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['OthCauses'] = pd.to_numeric(p_echipe['OthCauses']).fillna(0).map("{0:.2f}".format).astype(str) + '%'
p_echipe['OthMembers'] = pd.to_numeric(p_echipe['OthMembers']).fillna(0).map("{0:.2f}".format).astype(str) + '%'