import pandas as pd

covid_data = pd.read_csv('hw_covid/covid_data.csv')
#print(covid_data.head())

vaccinations_data = pd.read_csv('hw_covid/country_vaccinations.csv')
vaccinations_data = vaccinations_data[
    ['country', 'date', 'total_vaccinations', 
     'people_vaccinated', 'people_vaccinated_per_hundred',
     'people_fully_vaccinated', 'people_fully_vaccinated_per_hundred',
     'daily_vaccinations', 'vaccines']
]
#print(vaccinations_data.head())

#Группируем таблицу по дате и названию страны и рассчитываем суммарные показатели по всем регионам. Тем самым переходим от данных по регионам к данным по странам:
covid_data = covid_data.groupby(
    ['date', 'country'], 
    as_index=False
)[['confirmed', 'deaths', 'recovered']].sum()

#Преобразуем даты в формат datetime с помощью функции pd.to_datetime():
covid_data['date'] = pd.to_datetime(covid_data['date'])

#Создадим признак больных на данный момент (active). Для этого вычтем из общего числа зафиксированных случаев число смертей и число выздоровевших пациентов:
covid_data['active'] = covid_data['confirmed'] - covid_data['deaths'] - covid_data['recovered']

#Создадим признак ежедневного прироста числа заболевших, умерших и выздоровевших людей.
# Для этого отсортируем данные по названиям стран, а затем по датам. После этого произведём группировку по странам и
# рассчитаем разницу между «вчера и сегодня» с помощью метода diff():
covid_data = covid_data.sort_values(by=['country', 'date'])
covid_data['daily_confirmed'] = covid_data.groupby('country')['confirmed'].diff()
covid_data['daily_deaths'] = covid_data.groupby('country')['deaths'].diff()
covid_data['daily_recovered'] = covid_data.groupby('country')['recovered'].diff()
print(covid_data.head())

#В таблице vaccinations_data достаточно будет преобразовать столбцы в формат datetime:
vaccinations_data['date'] = pd.to_datetime(vaccinations_data['date'])


print(min(covid_data['date']), max(covid_data['date']))
print(min(vaccinations_data['date']), max(vaccinations_data['date']))

#С помощью метода merge() объедините таблицы covid_data и vaccinations_data по столбцам date и country.
# Тип объединения выставьте так, чтобы в результирующую таблицу попали только наблюдения за период,
# вычисленный в задании 3.1. То есть в результирующую таблицу должны попасть все записи из таблицы covid_data 
# и из её пересечения с vaccinations_data, но не более. Результат объединения занесите в переменную covid_df.

covid_df = covid_data.merge(
    vaccinations_data, 
    on = ['date', 'country'],
    how='left')
print(covid_df.info())
print('Число строк: ', covid_df.shape[0])
print('Число столбцов: ', covid_df.shape[1])

#создайте признаки death_rate — общий процент смертей среди зафиксированных случаев (летальность) 
# и recover_rate — общий процент случаев выздоровления. Данные характеристики рассчитайте как отношение числа смертей (deaths) 
# и числа выздоровлений (recovered) к числу зафиксированных случаев (confirmed) и умножьте результаты на 100%.
covid_df['death_rate'] = covid_df['deaths'] / covid_df['confirmed'] *100
covid_df['recover_rate'] = covid_df['recovered'] / covid_df['confirmed'] *100

#максимальная летальность в США (United States)
print(round(covid_df[covid_df['country'] == 'United States']['death_rate'].max(), 2))
#Чему равен средний процент выздоровевших в России (Russia)?
print(round(covid_df[covid_df['country'] == 'Russia']['recover_rate'].mean(), 2))

grouped_cases = covid_df.groupby('date')['daily_confirmed'].sum()
grouped_cases.plot(
    kind='line',
    figsize=(12, 4),
    title='Ежедневная заболеваемость по всем странам',
    grid = True,
    lw=3
)