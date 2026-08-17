import pandas as pd
import numpy as np
nascite=pd.read_csv('births.csv')
nascite.head()
nascite['decade']=10*(nascite['year']//10)
nascite.head()
nascite.pivot_table('births',index='decade',columns='gender',aggfunc='sum')
import matplotlib.pyplot as plt
%matplotlib
nascite.pivot_table('births',index='year',columns='gender',aggfunc='sum').plot()
plt.ylabel('nascite totali per anno per genere')

# DATA CLEANING--> rimuovere outliers (valori anomali)

nascite.describe() # min/max di births, max di day
nascite.isnull().any()

# sigma-clipping: 
# 1) ipotizza che dati siano distribuiti secondo distribuzione normale
# 2) si prova a stimare sigma e si eliminano le code (mediana-5sigma,mediana+5sigma)
# 3) nella normale sigma=(q3-q1)/1.35
# 4) i quartili non si stimano perchè non sensibili agli outliers
#esempio media-mediana: # a=np.random.randint(100,size=10)                                                                                                                                                                                                                                                                                                                                                                      
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

quartili = np.percentile(nascite['births'], [25, 50, 75])
quartili
mediana=quartili[1]
iqr=quartili[2]-quartili[0]
sigma=iqr/1.35

nascite_clean=nascite.loc[(nascite['births']<mediana+5*sigma) & (nascite['births']>mediana-5*sigma),:]


nascite_clean.isnull().any()

nascite.describe()
nascite_clean.describe()
