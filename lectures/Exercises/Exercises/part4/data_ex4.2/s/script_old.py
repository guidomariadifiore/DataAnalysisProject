import numpy as np
import pandas as pd
import seaborn as sns

births = pd.read_csv('births.csv')
print(births.head(),births.count())

births['decade'] = 10 * (births['year'] // 10)
print(births.pivot_table('births', index='decade', columns='gender', aggfunc='sum'))


import matplotlib.pyplot as plt
sns.set() # use Seaborn styles
births.pivot_table('births', index='year', columns='gender', aggfunc='sum').plot()
plt.ylabel('total births per year');

#plt.show()

# rimuovere outliers
quartiles = np.percentile(births['births'], [25, 50, 75])
mu = quartiles[1] # fare esempio media-mediana: a=np.random.randint(100,size=10)                                                                                                                                                                                                                                                                                                                                                                      
#Out[23]: array([58, 67, 81, 36, 45,  7, 87, 43, 49, 50])
#In [24]: np.mean(a)                                                                                                                                                                                         
#Out[24]: 52.3
#In [25]: np.median(a)                                                                                                                                                                                       
#Out[25]: 49.5
#In [26]: a[-1]=500                                                                                                                                                                                          
#In [27]: np.mean(a)                                                                                                                                                                                         
#Out[27]: 97.3
#In [28]: np.median(a)                                                                                                                                                                                       
#Out[28]: 53.5

sig = 0.74 * (quartiles[2] - quartiles[0]) # nella normale standard il rapporto tra dev.std(1) e range interquartile(1.35)=0.74
# range interquartile: differenza tra 3 quartile e 1 quartile (contiene meta' elementi)

births=births.loc[(births.births<mu+5*sig)&(births.births>mu-5*sig),:] 

births['day'] = births['day'].astype(int)

births.index = pd.to_datetime(10000 * births.year +100 * births.month + births.day, format='%Y%m%d')

births['dayofweek'] = births.index.dayofweek

import matplotlib.pyplot as plt
import matplotlib as mpl
births.pivot_table('births', index='dayofweek',
columns='decade', aggfunc='mean').plot()
plt.gca().set_xticklabels(['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
plt.ylabel('mean births by day')





