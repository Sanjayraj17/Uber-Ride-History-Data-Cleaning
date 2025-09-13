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

# Barplot for number of rides in day-night

sns.countplot(uber_df['day-night'], palette = 'coolwarm', edgecolor = 'black')
plt.xticks(rotation = 90)
plt.show()

# Number of rides per category in day-night

plt.figure(figsize = (10,6))

sns.countplot(x = 'CATEGORY*', hue = 'day-night', data = uber_df, palette = 'Set2', alpha = 1.0)
plt.xticks(rotation = 90)
plt.title('Categories by day-night')
plt.show()

plt.figure(figsize = (10,6))

sns.histplot( x = 'day-night', hue = 'CATEGORY*', data = uber_df,  palette = 'Set2', alpha = 1.0)
plt.xticks(rotation = 90)
plt.title('Proportion of Categories by day-night')
plt.show()

# Heatmap for visualizing purpose vs day-night

plt.figure(figsize = (10,5))

heatmap_data = uber_df.groupby(['PURPOSE*','day-night']).size().unstack()

sns.heatmap(heatmap_data, annot = True, cmap = 'YlGnBu', fmt = 'd', alpha = 1.0)

plt.title('Purpose vs Day-Night')

plt.show()

plt.figure(figsize = (10,5))

heatmap_data = uber_df.groupby(['PURPOSE*','day-night']).size().unstack()
total = heatmap_data.sum().sum()

sns.heatmap(heatmap_data, annot = heatmap_data.applymap(lambda x : f'{x}\n({x/total : .1%})'), cmap = 'YlGnBu', fmt = 's', alpha = 1.0)

plt.title('Purpose vs Day-Night')

plt.show()

# Pie plot for visualizing the percentage of rides by purpose

plt.figure(figsize = (8,8))

uber_df['CATEGORY*'].value_counts().plot.pie(autopct = "%1.1f%%", startangle = 90, cmap = 'Set3')

plt.ylabel(' ')

plt.show()

plt.figure(figsize = (8,8))

def autopct_with_counts(pct, values):
    total = sum(values)
    absolute = int(pct/100. * total)
    return f'{pct: .1f}%\n ({absolute})'
    
uber_df['CATEGORY*'].value_counts().plot.pie(autopct = lambda pct : autopct_with_counts(pct , uber_df['CATEGORY*'].value_counts()), startangle = 90, cmap = 'Set3')

plt.ylabel(' ')

plt.show()

# Boxplot for visualizing number of rides in day-night

plt.figure(figsize = (10,6))
sns.boxplot(data = uber_df, x = 'day-night', y = 'MILES*', palette = 'coolwarm')
plt.show()

# violin plot for visualizing purpose vs miles

plt.figure(figsize = (10,6))

sns.violinplot(data = uber_df, x = 'PURPOSE*', y ='MILES*', palette = 'muted')
plt.xticks(rotation = 90)
plt.show()

sns.set(style = 'whitegrid')
plt.figure(figsize = (10,6))

sns.violinplot(data = uber_df, x = 'day-night', y ='MILES*', palette = 'muted')
plt.xlabel('Day-Night')
plt.ylabel('Miles')
plt.title("Miles distribution by day-night")
plt.show()

# Barplot for purpose and miles with annotations

plt.figure(figsize = (10,6))

ax = sns.barplot(data = uber_df, x ='PURPOSE*', y = 'MILES*' ,estimator = sum , ci = None, palette = 'Set2')

for p in ax.patches:
    ax.annotate(f'{p.get_height() : .2f}', (p.get_x() + p.get_width() / 2. , p.get_height()), ha = 'center', va = 'center', xytext = (0,9), textcoords = 'offset points')
plt.xticks(rotation = 90)
plt.show()

# Scatter plot for miles vs category

plt.figure(figsize = (10,6))

sns.scatterplot(data = uber_df, x = 'time', y = 'MILES*', hue = 'CATEGORY*')

plt.title('Miles vs Category')

plt.show()

# creating a block of code for finding round trips

def round(x):
    if x['START*'] == x['STOP*']:
        return 'YES'
    else :
        return 'NO'

uber_df['ROUND_TRIP'] = uber_df.apply(round, axis = 1)

# visualizing the number of round trips

sns.countplot(uber_df['ROUND_TRIP'])
plt.show()

# Extracting month from the start date

uber_df['MONTH'] = pd.DatetimeIndex(uber_df['START_DATE*']).month
uber_df['MONTH']

#  Creating a dictionary for mapping the name of the month

dict = { 1:'jan', 2 :'feb',3:'mar',4:'apr',5:'may',6:'june',7:'july',8:'aug',9:'sep',10:'oct',11:'nov',12:'dec'}
uber_df['MONTH'] = uber_df['MONTH'].map(dict)

# Visualizing the number of rides in each month

plt.figure(figsize = (15,7))
sns.countplot(uber_df['MONTH'])
plt.show()

# Are theremore rides on weekday or weekend

uber_df['WEEKDAY'] = uber_df['START_DATE*'].dt.day_name()

plt.figure(figsize = (10,5))
sns.countplot(data = uber_df, x = 'WEEKDAY',order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],  palette = 'Set3')
plt.title('Rides on weekday')
plt.xlabel('Days')
plt.show()


# Rides across different month

sns.countplot(data = uber_df, x = 'MONTH', palette = 'Set3')
plt.title("Rides across different month")
plt.show()

# Rides by time of the day (peak hours)

sorted_time_counts = uber_df['time'].sort_values(ascending = False)

plt.figure(figsize = (10,6))

ax = sns.countplot( data = uber_df, x = 'time', order = sorted_time_counts, palette = 'viridis')

for p in ax.patches:
    ax.annotate(f'{p.get_height() : .1f}', (p.get_x() + p.get_width() / 2. , p.get_height()), ha = 'center', va = 'bottom')
plt.title('Rides by time of the day')

plt.show()

# Modifying the names of the column

uber_df.columns = uber_df.columns.str.replace('*','',regex = False).str.replace(' ','').str.lower().str.strip()

# Minimum and maximum time taken between rides in each category

uber_df['ride_duration'] = (uber_df['end_date'] - uber_df['start_date']).dt.total_seconds() / 60

duration_by_category = uber_df.groupby('category')['ride_duration'].agg(['min','max'])

duration_by_category

# Average ride in each day of the week

uber_df['weekday'] = uber_df['start_date'].dt.day_name()

rides_by_weekday = uber_df.groupby('weekday').size()

average = rides_by_weekday / uber_df['weekday'].nunique()

print(average)

# Average miles travelled in each period of a day

avg_miles = uber_df.groupby('day-night')['miles'].mean()
avg_miles

