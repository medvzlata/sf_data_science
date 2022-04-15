import pandas as pd
nlo_df = pd.read_csv('https://raw.githubusercontent.com/justmarkham/pandas-videos/master/data/ufo.csv')

#В каком году отмечается наибольшее количество случаев наблюдения НЛО в США?
nlo_df['Time'] = pd.to_datetime(nlo_df['Time'])
print(nlo_df['Time'].dt.year.mode()[0])

#Найдите средний интервал времени (в днях) между двумя последовательными случаями наблюдения НЛО в штате Невада (NV)
#Чтобы вычислить разницу между двумя соседними датами в столбце, примените к нему метод diff()
nlo_df["Date"] = nlo_df["Time"].dt.date
print(nlo_df[nlo_df['State'] == 'NV']['Date'].diff().dt.days.mean())