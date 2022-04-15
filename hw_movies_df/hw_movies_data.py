import pandas as pd

mov_df = pd.read_csv('hw_movies_df/ratings_movies.csv')
#print(m_mov_df['userId'].nunique())

#m_dat_df = pd.read_csv('hw_movies_df/dates.csv', sep=',')
#m_dat_df['date_year'] = pd.to_datetime(m_dat_df['date']).dt.year
#print(print(m_dat_df['date_year'].mode()))
#библиотека для регулярных выражений
import re 
def get_year_release(arg):
    #находим все слова по шаблону "(DDDD)"
    candidates = re.findall(r'\(\d{4}\)', arg) 
    # проверяем число вхождений
    if len(candidates) > 0:
        #если число вхождений больше 0,
	#очищаем строку от знаков "(" и ")"
        year = candidates[0].replace('(', '')
        year = year.replace(')', '')
        return int(year)
    else:
        #если год не указан, возвращаем None
        return None
mov_df['year_release'] = mov_df['title'].apply(get_year_release)
print(mov_df.info())
print(mov_df.head())

#Какой фильм, выпущенный в 1999 году, получил наименьшую среднюю оценку зрителей?
print(mov_df[mov_df['year_release'] == 1999].groupby('title')['rating'].mean().sort_values())

#Какое сочетание жанров фильмов (genres), выпущенных в 2010 году, получило наименьшую среднюю оценку (rating)?
print(mov_df[mov_df['year_release'] == 2010].groupby('genres')['rating'].mean().sort_values())

#Какой пользователь (userId) посмотрел наибольшее количество различных (уникальных) жанров (genres) фильмов? В качестве ответа запишите идентификатор этого пользователя.
print(mov_df.groupby('userId')['genres'].nunique().sort_values(ascending=False))

#Найдите пользователя, который выставил наименьшее количество оценок, но его средняя оценка фильмам наибольшая.
print(mov_df.groupby('userId')['rating'].agg(['count', 'mean']).sort_values(by=['count','mean'], ascending=[True, False]))

#Найдите сочетание жанров (genres) за 2018 году, которое имеет наибольший средний рейтинг (среднее по столбцу rating), 
# и при этом число выставленных ему оценок (количество значений в столбце rating) больше 10
print(mov_df[mov_df['year_release'] == 2018].groupby('genres')['rating'].agg(['count', 'mean']).sort_values(by=['count','mean'], ascending=[False, False]))
#mask = joined['year_release'] == 2018
#grouped = joined[mask].groupby('genres')['rating'].agg(['mean', 'count'])
#grouped[grouped['count']>10].sort_values(by='mean', ascending=False)

#Добавьте в таблицу новый признак year_rating — год выставления оценки.
# Создайте сводную таблицу, которая иллюстрирует зависимость среднего рейтинга фильма от года выставления оценки и жанра. 
mov_df['year_rating']=pd.to_datetime(mov_df['date']).dt.year
print(mov_df.pivot_table(
    values='rating',
    index='year_rating',
    columns='genres',
    aggfunc='mean',
    fill_value=0
))
