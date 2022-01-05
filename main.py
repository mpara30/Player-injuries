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

# Sortare descrescatoare a echipelor in functie de InjuryNumbers
print((injury[['TeamName', 'InjuryNumbers']].copy()).sort_values(by = ['InjuryNumbers'], ascending=False))

# Stacked bar pe echipe
culori_stack = ['darkorange', 'royalblue', 'silver', 'red', 'forestgreen', 'chocolate', 'plum', 'aqua',
                'gold', 'tomato', 'springgreen', 'darkkhaki', 'indigo', 'deeppink', 'steelblue']
injury.plot(x='Abbreviation', y = injuries_list, color = culori_stack, kind='bar', stacked=True,
            title='Grafic Stacked Bar a tipurilor de accidentari pe echipe')
plt.legend(loc = 'best', frameon = False, ncol = 2)
plt.yticks(np.arange(0, 70, 5))
plt.show()

# Sortare tipuri de accidentari pentru fiecare echipa
acc_dframe = injury.drop(injury.columns[[0, 2, 3, 4]], axis=1).copy().set_index('Abbreviation')
inj_lst = [[z for z,p in sorted(zip(acc_dframe.columns.values.tolist(), x), key=lambda y: y[1], reverse=True)]
      for x in acc_dframe.apply(lambda x : x.rank(),1).values.tolist()]
print(pd.Series(data=inj_lst,index=acc_dframe.index))

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
new_injury = pd.read_csv("Injuries_Updated.csv")
print(new_injury.select_dtypes(np.number).sum().rename('TOTAL').sort_values(ascending=False))

# Adaugare valori TOTAL ca rand in DataFrame
new_injury.loc[len(new_injury.index)] = new_injury.select_dtypes(np.number).sum()
new_injury = new_injury.drop(new_injury.iloc[:, 0:4], axis=1).copy().\
    rename(index = {new_injury.index[20]:"TOTAL"}).astype(int)
print(new_injury)
new_injury.to_csv("Injuries_with_TOTAL.csv")

# Creare DataFrame doar cu totalul fiecarei categorii in parte
new_injury_total = new_injury.loc["TOTAL"].reset_index()
new_injury_total = new_injury_total.rename(columns={new_injury_total.columns[0]:'Categories'}).reset_index(drop=True)
new_injury_total['Percent'] = (new_injury_total['TOTAL']/new_injury_total.iloc[0, 1]*100).map('{:.2f}'.format).astype(float)
new_injury_total = new_injury_total.drop(0, axis = 0)
print(new_injury_total)

#Grafic Bar Chart pentru afisarea procentelor aferente fiecarei categorii
# raportat la numarul total de accidentari
x = new_injury_total['Categories']
y = new_injury_total['Percent']
plt.yticks(np.arange(0, y.max(), 2.5))
for bar in plt.bar(x, height = y, width=.5, color=culori_stack):
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .2, yval)
plt.title("Procentajul tipurilor de accidentari raportat la numarul total")
plt.show()

# Grafic bar-chart pt valorile fiecarui tip principal de accidentare dintr-o echipa
injury.plot.bar(x = 'Abbreviation', y = ['Knee','Knock','Thigh'],
               title = 'Bar Chart al accidentarilor importante pentru fiecare echipa')
plt.yticks(np.arange(0, 31, 2))
plt.show()

# Grafic heatmap pt a vedea corelatia dintre accidentari
sb.heatmap(injury.corr().loc['Ankle':'OthMembers', 'Ankle':'OthMembers'], cmap='coolwarm', annot=True).
set(title = 'Corelograma a accidentarilor')
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
culori_echipe = ['red', 'maroon', 'dodgerblue', 'indianred', 'mediumblue',
                 'cornflowerblue', 'blue', 'gainsboro', 'gold', 'mediumpurple',
                 'crimson', 'deepskyblue', 'red', 'black', 'indianred',
                 'mistyrose', 'navy', 'yellowgreen', 'maroon', 'darkorange']
plt.yticks(np.arange(0, y.max(), 5))
for bar in plt.bar(x, height = y, width=.6, color=culori_echipe):
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .5, yval)
plt.title("Procentajul jucatorilor accidentati in functie de echipa")
plt.show()
