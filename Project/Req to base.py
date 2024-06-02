import pandas as pd
#Запросы:
#1. Выбрать все новости, в заголовке которых фигурирует слово "США" в период, указанный в программе.
#2. Подсчитать за каждый день выборки количество новостей, и количество новостей со словом "США"
#UPD: Полную дату, категорию и количество просмотров можно найти в каждой новости, если перейти на неё


df = pd.read_excel('РБК.xlsx')

USA_news = df['Заголовок'].str.contains('США')
count_USA_news = df['Заголовок'].str.contains('США').sum()
print(USA_news)
print(f'Количество новостей с США: {count_USA_news}')

print(df['Заголовок'].str.count('Яндекс'))
print(df['Заголовок'].str.contains('Яндекс').sum())

df['Дата'] = pd.to_datetime(df['Дата']).dt.strftime('%Y-%m-%d')
print('Подсчёт всех новостей')
print(df.groupby('Дата').size().reset_index(name='total_news'))
print('Подсчёт всех новостей с США')
print(df[df['Заголовок'].str.contains('США')].groupby('Дата').size().reset_index(name='usa_news'))
print('Подсчёт всех новостей с Яндекс')
print(df[df['Заголовок'].str.contains('Яндекс')].groupby('Дата').size().reset_index(name='usa_news'))