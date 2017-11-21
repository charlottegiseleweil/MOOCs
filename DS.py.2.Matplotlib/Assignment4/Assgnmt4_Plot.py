import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 

mariages = pd.read_csv('data/mariages.csv', sep=';')
divorces = pd.read_csv('data/divorces.csv', sep=';')
population = pd.read_csv('data/WorldBankPop.csv', sep=',')
population = population.transpose()

mariages.columns = ['Yr','Mariages','Suisses_m','Suisse+foreign','Suissesse+foreign','foreigners'] #Full data starts 1885
divorces.columns = ['Yr','Divorces','Suisses_d','Suisse+foreign','Suissesse+foreign','foreigners'] #Full data starts 1933

mariages.set_index('Yr', inplace=True) 
divorces.set_index('Yr', inplace=True)

merged = pd.merge(mariages, divorces, how='outer',left_index=True,right_index=True)
# ----- ----- ----- -----
# ----- Figure ----- ----
# ----- ----- ----- -----

merged.plot(linewidth=2.6,figsize=(20,7),color=['#4354d8',"#751069"])

print(population)
# Aesthetics 
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.margins(x=0,y=0)
start, end = ax.get_xlim()
start = start - 1
ax.xaxis.set_ticks(np.arange(start, end, 10))
plt.ylabel('#/year', alpha=0.8)
plt.xlabel(' ')
plt.title('Mariages & Divorces in Switzerland', alpha=0.8,fontsize=20,fontstyle='italic')

# Additions and Labels
plt.axhline(19000,xmin=((1914-start)/(end-start)),xmax=((1918-start)/(end-start)),color='grey', linewidth =4)
plt.axhline(30000,xmin=((1939-start)/(end-start)),xmax=((1945-start)/(end-start)),color='grey', linewidth =4)
plt.text(1919, 18500, 'World War 1',style='italic', color='grey')
plt.text(1946, 29500, 'World War 2',style='italic', color='grey')

plt.axvline(1971,ymin=0.1,ymax=0.97,linewidth=2,color='#d79ed8')
plt.text(1962, 3000, "1971: Women's right to vote",style='italic',color='#d79ed8')

plt.show()
#plt.savefig('Assgnmt4.jpg')
