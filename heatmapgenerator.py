import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import csv

import july
from july.utils import date_range



#dates = date_range((datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d'), datetime.today().strftime('%Y-%m-%d'))
#data = np.random.randint(0, 14, len(dates))

datePomCounts = {}

with open('./data/pomodoro/history.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        d = row['End Date']
        if d in datePomCounts:
            datePomCounts[d] += 1
        else:
            datePomCounts[d] = 1
print(datePomCounts)

dates = pd.date_range((datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d'), datetime.today().strftime('%Y-%m-%d'))
values = []
for date in dates:
    dateString = date.strftime('%Y-%m-%d')
    #print(dateString)
    if dateString in datePomCounts:
        print("date match")
        values.append(datePomCounts[dateString])
    else:
        values.append(0)
print(values)

july.heatmap(dates, values, title='Pomodoro Activity', cmap="july")
plt.savefig("./data/pomodoro/pomodoro.svg")
#
#lesley.cal_heatmap(dates, values).save("./data/pomodoro/pomodoro.svg")
