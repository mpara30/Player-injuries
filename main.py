import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
injury = pd.read_csv("Injuries Databases.csv")
print(injury, sep="\n")

# Adaugare coloana 'InjuryNumbers'
injuries_list = ["Ankle", "Back", "Calf", "COVID19", "Foot", "Groin", "Hamstring", "Head", "Knee", "Knock",
                "Muscles", "Shoulder", "Thigh", "OthCauses", "OthMembers"]

sum_injuries = injury[injuries_list].sum(axis = 1)
injury.insert(4, 'InjuryNumbers', sum_injuries)
injury.to_csv("Injuries_Updated.csv")

# Calcul procente
def c_proc():

    valori = []
    for i in range(len(injury)):
        _v = []
        for (j, k) in zip(injuries_list, range(len(injuries_list))):
            f_proc = float((injury[j][i] / injury["InjuryNumbers"][i]) * 100)
            _v.append(f_proc)
        valori.append(_v)

    return np.array(valori)

proc_echipe = c_proc()
print(proc_echipe)

# Salvare valori in tabel
p_echipe = pd.DataFrame(data=proc_echipe, index=injury["Abbreviation"], columns=injuries_list)
print(p_echipe)
p_echipe.to_csv("Percentages per teams.csv")

# Convertire valori in procente
new_pechipe = p_echipe.applymap('{:.2f}'.format).astype(float)
print(new_pechipe)

# Salvare valori noi
new_pechipe.to_csv("Aprox. Percentages per teams.csv")

# Calcul total pentru coloanele numerice
new_injury = pd.read_csv("Injuries Databases.csv")
total_sume = new_injury.select_dtypes(np.number).sum().rename('TOTAL')
new_injury.loc[len(new_injury.index)] = total_sume
new_injury = new_injury.rename(index = {new_injury.index[20]:"TOTAL"})
print(new_injury)
new_injury.to_csv("Injuries_with_TOTAL.csv")

# Sortare sume totale descrescator
sort_desc = total_sume.sort_values(ascending=False)
print(sort_desc)

# Grafic bar-chart pt valorile fiecarui tip principal de accidentare dintr-o echipa
injury.plot.bar(x = 'Abbreviation', y = ['Ankle','Calf','COVID19','Groin','Knee','Knock','Thigh'])
plt.show()

# Grafic heatmap pt a vedea corelatia dintre accidentari
sb.heatmap(injury.corr().loc['Ankle':'OthMembers', 'Ankle':'OthMembers'], cmap='coolwarm', annot=True)
plt.show()

# Calcul procentaj al jucatorilor accidentati
inj_numb_perc = (injury['InjuredPlayers'] / injury['PlayerNumbers']) * 100
print(inj_numb_perc)
# Adaugare coloana noua in tabel
injury['Inj_Numb_Perc'] = inj_numb_perc.map('{:.2f}'.format).astype(float)
print(injury)
# Grafic barchart pt procentajul jucatorilor accidentati
x = injury['Abbreviation']
y = injury['Inj_Numb_Perc']
plt.yticks(np.arange(0, y.max(), 5))
for bar in plt.bar(x, height = y, width=.6, color=['red', 'maroon', 'dodgerblue', 'indianred', 'mediumblue',
                                                   'cornflowerblue', 'blue', 'gainsboro', 'gold', 'mediumpurple',
                                                   'crimson', 'deepskyblue', 'red', 'black', 'indianred',
                                                   'mistyrose', 'navy', 'yellowgreen', 'maroon', 'darkorange']):
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .5, yval)
plt.show()
