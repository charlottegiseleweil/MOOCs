
# coding: utf-8

#User specified parameter: Y-value
Y = 41000

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
import scipy.stats as ss


#Data
np.random.seed(12345)
df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

#Bar plot with error bars (95% Confidence interval)
ci = 0.95
means = df.transpose().mean()
stds = df.transpose().std()
n = df.shape[1]
C = ss.t.ppf(1-((1-ci)/2), n-1)
std_error = stds/np.sqrt(n)
margin_of_error = std_error * C

#Colors of the bars according to Y value
nearest = 100
df_colors = pd.DataFrame()
df_colors['diff'] = nearest * ((Y - means)//nearest)
df_colors['sign'] = df_colors['diff'].abs()/df_colors['diff']

old_range = abs(df_colors['diff']).min(), abs(df_colors['diff']).max()
new_range = .5 , 1
df_colors['shade'] = df_colors['sign'] * np.interp(abs(df_colors['diff']), old_range, new_range)

df_colors['select'] = df_colors['shade'].apply(lambda x: 'white' if x==0 else cm.Blues(abs(x)) if x>0 else cm.Reds(abs(x)) )

#Bar plot
#bars = plt.bar(np.arange(len(df.index)), means, color=df_colors['select'],width=0.99, align='center', yerr=margin_of_error)


#Bar plot
fig = plt.figure()
bars = fig.add_subplot(1,1,1)
bars.bar(np.arange(len(df.index)), means, color=df_colors['select'],width=0.99, align='center', yerr=margin_of_error)

#Horizontal line at Y-value
plt.axhline(Y,color='grey', linewidth =4)
plt.text(1.02, 4.2e4, Y, va='center', ha="left", bbox=dict(facecolor="w",alpha=0.5),transform=bars.get_yaxis_transform())

#Style
plt.xticks(np.arange(len(df.index)), df.index, alpha=0.8,color='black')
plt.ylabel('Chosen Y value is {}'.format(Y), alpha=0.8)
plt.title('Which of these distribution is more likely to contain this Y data?', alpha=0.8)

#Legend colorscale oooooo
#cmap = mpl.colors.ListedColormap(['b', 'w', 'r'])
#cmap.set_over('0.25')
#cmap.set_under('0.75')
#bounds = [1, 3, 4, 6]
#norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
#legend = mpl.colorbar.ColorbarBase(bars, cmap=cmap,
#                                norm=norm,
#                                boundaries=[0] + bounds + [13],
#                                extend='both',
#                                ticks=bounds,  # optional
#                                spacing='proportional',
#                                orientation='horizontal')
#legend.set_label('Discrete intervals, some other units')
#plt.colorbar()
#cax = bars.imshow(means, interpolation='nearest', cmap=Blues + Reds)
#cbar = fig.colorbar(df_colors['select'], ticks=[-1, 0, 1], orientation='horizontal')
#cbar.ax.set_xticklabels(['Low', 'Medium', 'High']) 

#plt.show()
fig.savefig('Assgnmt3_1.jpg')

## Additional snippets of code for harder options
#Interactive Y value
# class PointPicker(object):
#     def __init__(self, bars, clicklim=2):
#         self.fig=bars.figure
#         self.bars = bars
#         self.clicklim = clicklim
#         self.horizontal_line = bars.axhline(y=.5, color='y', alpha=0.5)
#         self.text = bars.text(0,0.5, "")
#         print self.horizontal_line
#         self.fig.canvas.mpl_connect('button_press_event', self.onclick)


#     def onclick(self, event):
#         if event.inaxes == self.bars:
#             x = event.xdata
#             y = event.ydata
#             xlim0, xlim1 = bars.get_xlim()
#             if x <= xlim0+(xlim1-xlim0)*self.clicklim:
#                 self.horizontal_line.set_ydata(y)
#                 self.text.set_text(str(y))
#                 self.text.set_position((xlim0, y))
#                 self.fig.canvas.draw()

# p = PointPicker(bars)

# #Update upon move
# def update(Y):
#     axline.set_ydata(Y)
#     for bar in bars:
#         bar.set_color(df_colors['select'])

# #update once before showing
# update(Y)

# def onMouseMove(event):
#     if event.inaxes == ax:
#         update(event.ydata)
#         fig.canvas.draw_idle()

# fig.canvas.mpl_connect('motion_notify_event', onMouseMove)
