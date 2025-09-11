# importing libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# loading dataset

uber_df = pd.read_csv('uberdrive.csv')

# shape of the dataset

uber_df.shape

# Data Preprocessing

uber_df.isnull().sum()
uber_df['PURPOSE*'].fillna('NOT', inplace = True)

# Check for dupicates

uber_df[uber_df.duplicated()]

# Data visualization

uber_df['START_DATE*'] = pd.to_datetime(uber_df['START_DATE*'], errors = 'coerce')
uber_df['END_DATE*'] = pd.to_datetime(uber_df['END_DATE*'], errors = 'coerce')

from datetime import datetime

uber_df['date'] = pd.DatetimeIndex(uber_df['START_DATE*']).date

uber_df['time'] = pd.DatetimeIndex(uber_df['START_DATE*']).hour

uber_df['day-night'] = pd.cut(x = uber_df['time'] , bins = [0,10,15,19,24], labels = ['Morning','Afternoon','Evening','Night'])

# Barplot for miles travelles

sns.histplot(uber_df['MILES*'],bins = 20, color = 'red', edgecolor = 'black', alpha = 0.5)
plt.show()

# total number of first 10 start locations

pd.value_counts(uber_df['START*']).iloc[:10].index
sns.countplot(y = 'START*' ,  order= pd.value_counts(uber_df['START*']).iloc[:10].index, data = uber_df)

plt.show()
