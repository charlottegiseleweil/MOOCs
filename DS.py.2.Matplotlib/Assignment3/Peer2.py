import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import pylab

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650),
                   np.random.normal(43000,100000,3650),
                   np.random.normal(43500,140000,3650),
                   np.random.normal(48000,70000,3650)],
                  index=['1992','1993','1994','1995'])

df=df.T

df_mean = df.mean()
df_std = df.std()/np.sqrt(len(df))

x = [1,2,3,4]

y0=eval(input('Give me your preferred y: '))
y = [y0]*5

my_colors = []
for i in range (4):
    z = 1992+i
    if (df_mean[i]-df_std[i] > y0):
        my_colors.append('darkred')
    elif (df_mean[i]-df_std[i] <= y0) & (df_mean[i]+df_std[i] >= y0):
        my_colors.append('w')
    else:
        my_colors.append('navy')

my_edgecolors = ['k']*4

labels = ['1992','1993','1994','1995']

plt.bar(x, df.mean(), color = my_colors, edgecolor = my_edgecolors, yerr = df_std, error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2))
plt.gca().get_xaxis().set_ticks(x)
plt.gca().set_xticklabels(labels)
plt.gca().set_yticks([y0], minor=True)
plt.grid(which='minor', alpha=1.0)
plt.text(-0.1,y0,str(y0),bbox=dict(boxstyle="round"),alpha=1)

plt.show()