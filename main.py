# Importare librarii
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import squarify as sq

# I. Citire si editare a fisierului original

# 1.1. Citire fisier
pd.set_option('display.max_columns', None)
injury = pd.read_csv("Injuries Databases.csv", index_col=False)
print(injury, sep="\n")

# 1.2. Adaugare coloana 'InjuryNumbers'
injuries_list = ["Ankle", "Back", "Calf", "COVID19", "Foot", "Groin", "Hamstring", "Head", "Knee", "Knock",
                "Muscles", "Shoulder", "Thigh", "OthCauses", "OthMembers"]
sum_injuries = injury[injuries_list].sum(axis = 1)
injury.insert(4, 'InjuryNumbers', sum_injuries)
print(injury)
injury.to_csv("Injuries_Updated.csv", index=False)

# 1.3. Sortare descrescatoare a echipelor in functie de InjuryNumbers
print((injury[['TeamName', 'InjuryNumbers']].copy()).sort_values(by = ['InjuryNumbers'], ascending=False))

# 1.4. Creare grafic Stacked bar pe echipe
culori_stack = ['darkorange', 'royalblue', 'silver', 'red', 'forestgreen', 'chocolate', 'violet', 'aqua',
                'gold', 'tomato', 'springgreen', 'darkkhaki', 'skyblue', 'pink', 'steelblue']
injury.plot(x='Abbreviation', y = injuries_list, color = culori_stack, kind='bar', stacked=True,
            title='Grafic Stacked Bar al tipurilor de accidentari, pentru fiecare echipa')
plt.legend(loc = 'best', frameon = False, ncol = 2)
plt.yticks(np.arange(0, 70, 5))
plt.show()

# 1.5. Sortare tipuri de accidentari pentru fiecare echipa
acc_dframe = injury.drop(injury.columns[[0, 2, 3, 4]], axis=1).copy().set_index('Abbreviation')
inj_lst = [[z for z,p in sorted(zip(acc_dframe.columns.values.tolist(), x), key=lambda y: y[1], reverse=True)]
      for x in acc_dframe.apply(lambda x : x.rank(),1).values.tolist()]
print(pd.Series(data=inj_lst,index=acc_dframe.index))

# II. Creare DataFrame cu procentele fiecarui tip de accidentare,
# raportat la nr total al lor, pt fiecare echipa in parte

# 2.1. Functie de calcul al procentelor
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

# 2.2. Salvare valori in tabel
p_echipe = pd.DataFrame(data=proc_echipe, index=injury["Abbreviation"], columns=injuries_list)
print(p_echipe)
p_echipe.to_csv("Percentages per teams.csv")

# 2.3. Convertire valori la 2 zecimale si salvare in alt tabel
print(p_echipe.applymap('{:.2f}'.format).astype(float))
(p_echipe.applymap('{:.2f}'.format).astype(float)).to_csv("Aprox. Percentages per teams.csv")

# 2.4. Importare date din noul DataFrame
perc_teams = pd.read_csv("Aprox. Percentages per teams.csv", index_col=False)
print(perc_teams)

# 2.5. Creare grafic horizontal stacked bar doar pentru o echipa
echipa_graf = perc_teams[perc_teams['Abbreviation'] == input("Choose the team by its Abbreviation: ")]
single_graf = echipa_graf.plot(x='Abbreviation', y= injuries_list, color = culori_stack, kind = 'barh',
             stacked=True, width=.03, figsize=(6, 5),  alpha = .85)
for c in single_graf.containers:
    single_graf.bar_label(c, labels = [f'{w:.2f}' if (w := v.get_width()) > 0 else '' for v in c],
                          fontsize=7, label_type='center')
single_graf.set_xlabel('Procente (%)', fontsize = 10)
single_graf.set_title("Procentaj al accidentarilor, raportat la numarul lor total, pentru fiecare echipa")
plt.legend(loc = 'best', ncol = 2)
plt.show()

# 2.6. Creare grafic horizontal stacked bar pentru toate echipele
multiple_graf = perc_teams.plot(x='Abbreviation', y= injuries_list, color = culori_stack, kind = 'barh',
             stacked=True, width=.8, mark_right = True, alpha = .8)
for c in multiple_graf.containers:
    multiple_graf.bar_label(c, labels = [f'{w:.2f}' if (w := v.get_width()) > 0 else '' for v in c],
                            fontsize=6.5, label_type='center')
multiple_graf.set_xlabel('Procente (%)')
multiple_graf.set_title("Procentaj al accidentarilor, raportat la numarul lor total, pentru fiecare echipa")
plt.legend(bbox_to_anchor=(1, 1), loc='upper left',  ncol = 1)
plt.show()

# III. Creare DataFrame pentru totalul fiecarei categorii in parte

# 3.1. Calcul total pentru coloanele numerice
new_injury = pd.read_csv("Injuries_Updated.csv")
print(new_injury.select_dtypes(np.number).sum().rename('TOTAL').sort_values(ascending=False))

# 3.2. Adaugare valori TOTAL ca rand in DataFrame
new_injury.loc[len(new_injury.index)] = new_injury.select_dtypes(np.number).sum()
new_injury = new_injury.rename(index = {new_injury.index[20]:"TOTAL"})
print(new_injury)
new_injury.to_csv("Injuries_with_TOTAL.csv", index=False)

# 3.3. Creare DataFrame doar cu totalul fiecarei categorii in parte
new_injury = new_injury.drop(new_injury.iloc[:, 0:4], axis=1).copy().astype(int)
new_injury_total = new_injury.loc["TOTAL"].reset_index()
new_injury_total = new_injury_total.rename(columns={new_injury_total.columns[0]:'Categories'}).reset_index(drop=True)
new_injury_total['Percent'] = (new_injury_total['TOTAL']/new_injury_total.iloc[0, 1]*100).map('{:.2f}'.format).astype(float)
new_injury_total = new_injury_total.drop(0, axis = 0)
print(new_injury_total)

# IV. Analiza pe grafice

# 4.1. Creare grafice pentru afisarea procentelor aferente fiecarei categorii
# raportat la numarul total de accidentari
# 4.1.1. Grafic Bar Chart
x = new_injury_total['Categories']
y = new_injury_total['Percent']
plt.yticks(np.arange(0, y.max(), 2.5))
for bar in plt.bar(x, height = y, width=.5, color=culori_stack):
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .2, yval)
plt.xticks(rotation=45, horizontalalignment='right', fontweight='light', fontsize=10)
plt.title("Procentajul tipurilor de accidentari, raportat la numarul lor total")
plt.show()
# 4.1.2. Grafic Treemap
lbl_tree = [f'{el[0]} = {el[1]}%' for el in zip(new_injury_total['Categories'], new_injury_total['Percent'])]
plt.figure(figsize=(12,8), dpi= 80)
sq.plot(sizes = new_injury_total['Percent'], label = lbl_tree, color = culori_stack, alpha=.7)
plt.title('Grafic Treemap pentru afisarea procentelor de accidentari, raportat la total', fontsize = 14)
plt.axis('off')
plt.show()

# 4.2. Grafic bar-chart pt valorile fiecarui tip principal de accidentare dintr-o echipa
injury.plot.bar(x = 'Abbreviation', y = ['Ankle','Knock','Thigh'],
                title = 'Bar Chart al categoriilor principale de accidentari')
plt.yticks(np.arange(0, 31, 2))
plt.show()

# 4.3. Grafic heatmap pt corelatia dintre accidentari
sb.heatmap(injury.corr().loc['Ankle':'OthMembers', 'Ankle':'OthMembers'], cmap='coolwarm', annot=True).\
    set(title = 'Corelograma a accidentarilor')
plt.xticks(rotation=40, ha="right")
plt.show()

# 4.4. Grafic bar-chart pt procentajul jucatorilor accidentati
# 4.4.1. Adaugare coloana noua in tabel cu calcul procentaj al jucatorilor accidentati
injury['Player_Inj_Perc'] = ((injury['InjuredPlayers'] / injury['PlayerNumbers']) * 100)\
    .map('{:.2f}'.format).astype(float)
print(injury)
# 4.4.2. Creare grafic
x = injury['Abbreviation']
y = injury['Player_Inj_Perc']
culori_echipe = ['red', 'maroon', 'dodgerblue', 'indianred', 'mediumblue',
                 'cornflowerblue', 'blue', 'gainsboro', 'gold', 'mediumpurple',
                 'crimson', 'deepskyblue', 'red', 'black', 'indianred',
                 'mistyrose', 'navy', 'yellowgreen', 'maroon', 'darkorange']
plt.yticks(np.arange(0, y.max(), 10))
for bar in plt.bar(x, height = y, width=.7, color=culori_echipe):
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .5, yval)
plt.title("Procentajul jucatorilor accidentati, in functie de echipa")
plt.show()

# V. Creare DataFrame cu noile date si clasamentul campionatului

# 5.1. Creare clasament echipe in functie de nr accidentari
inj_numb_class = (injury[['TeamName', 'InjuryNumbers']].copy()).\
    sort_values(by = ['InjuryNumbers'], ascending=False).reset_index(drop=True)
inj_numb_class['Inj_Numb_Pos'] = [i for i in range(1, 21)]
print(inj_numb_class)

# 5.2. Creare clasament echipe in functie de procentajul nr de accidentati
player_inj_perc_class = (injury[['TeamName', 'Player_Inj_Perc']].copy()).\
    sort_values(by = ['Player_Inj_Perc'], ascending=False).reset_index(drop=True)
player_inj_perc_class['Player_Inj_Perc_Pos'] = [i for i in range(1, 21)]
print(player_inj_perc_class)

# 5.3. Creare DataFrame clasament final
BPL_data = {
    'Clas_Pos':[i for i in range(1, 21)],
    'TeamName': ['Manchester City', 'Manchester United', 'Liverpool', 'Chelsea', 'Leicester City',
                 'West Ham United', 'Tottenham Hotspur', 'Arsenal', 'Leeds United', 'Everton',
                 'Aston Villa', 'Newcastle United', 'Wolverhampton Wanderers', 'Crystal Palace',
                 'Southampton', 'Brighton & Hove Albion', 'Burnley', 'Fulham',
                 'West Bromwich Albion', 'Sheffield United'],
    'Points':[86, 74, 69, 67, 66, 65, 62, 61, 59, 59, 55, 45, 45, 44, 43, 41, 39, 28, 26, 23],
    'Win':[27, 21, 20, 19, 20, 19, 18, 18, 18, 17, 16, 12, 12, 12, 12, 9, 10, 5, 5, 7],
    'Draw':[5, 11, 9, 10, 6, 8, 8, 7, 5, 8, 7, 9, 9, 8, 7, 14, 9, 13, 11, 2],
    'Lose':[6, 6, 9, 9, 12, 11, 12, 13, 15, 13, 15, 17, 17, 18, 19, 15, 19, 20, 22, 29],
    'Gls_Dif':[+51, +29, +26, +22, +18, +15, +23, +16, +8, -1, +9, -16,
               -16, -25, -21, -6, -22, -26, -41, -43]
}
BPL_class = pd.DataFrame(BPL_data)
print(BPL_class)

# 5.4. Creare DataFrame final prin join si salvare a acestuia
tabel_final = pd.merge(pd.merge(BPL_class, inj_numb_class, on = 'TeamName'),
                       player_inj_perc_class, on = 'TeamName')
print(tabel_final)
tabel_final.to_csv('BPL_Ranking.csv', index=False)
