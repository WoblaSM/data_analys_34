import pandas as pd
import random
df = pd.read_csv('Данные по использованию климатических систем.csv', delimiter=';', skipinitialspace=True, decimal=',')
df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.lower()
df['возраст'] = df['возраст'].astype(float)
df['оценка_комфорта'] = df['оценка_комфорта'].astype(float)
df['температура_воздуха_в_помещении'] = df['температура_воздуха_в_помещении'].astype(float)
df['скорость_воздуха'] = df['скорость_воздуха'].astype(float)
df['среднемесячная_температура_на_улице'] = df['среднемесячная_температура_на_улице'].astype(float)
df['rh'] = df['rh'].astype(float)
df['утепление'] = df['утепление'].astype(float)
df['температура_воздуха_на_улице'] = df['температура_воздуха_на_улице'].astype(float)
df['ощущение_температуры'] = df['ощущение_температуры'].astype(float)
df['скорость_воздуха'] = df['скорость_воздуха'].astype(float)
df['климат'] = df['климат'].replace('Cубтроп океанич', 'Cубтропический океанический')
df['предпочтительное_изменение_температуры'] = df['предпочтительное_изменение_температуры'].replace('Холодн', 'Холоднее')
df['предпочтительное_изменение_температуры'] = df['предпочтительное_изменение_температуры'].replace('Тепле', 'Теплее')
# Посмотрим где есть пропуски
for i in df.columns:
    print(i)
    print(any(df[i].isnull()))
print()
# В столбце режим_при_смешанном_типе_охлаждения нужно проверить пропуски только при
# смешанном типе охлаждения отфильтруем значения и проверим ещё раз
s1 = df[df['способ_охлаждения'] == 'Смешанный']
print('режим_при_смешанном_типе_охлаждения')
print(any(s1['режим_при_смешанном_типе_охлаждения'].isnull()))
df['режим_при_смешанном_типе_охлаждения'] = df['режим_при_смешанном_типе_охлаждения'].fillna('Не_смешанный')
df['способ_обогрева'] = df['способ_обогрева'].fillna('Нет')
# Заполним пропуски в столбце пол у нас нет данных ни по городу Техас ни по другим городам США.
# Мы не можем заполнить эти пропуски групповой модой. Тогда заполним эти данные случайным
# образом сохранив соотношение мужчин и женщин
# m = df[df['пол'] == 'Мужской']['пол'].count()
# w = df[df['пол'] == 'Женский']['пол'].count()
# al = m + w
# na = len(df) - al
# per = w / al
# lst = []
# for i in range(na):
#     rnd = random.random()
#     if rnd <= per:
#         lst.append('Женский')
#     else:
#         lst.append('Мужской')
lst = ['Женский', 'Мужской', 'Мужской', 'Мужской', 'Женский', 'Мужской', 'Женский', 'Женский', 'Мужской', 'Мужской',
       'Мужской', 'Женский', 'Женский', 'Мужской', 'Женский', 'Женский', 'Мужской', 'Женский', 'Мужской', 'Женский',
       'Мужской', 'Мужской', 'Мужской', 'Мужской', 'Мужской', 'Женский', 'Мужской', 'Мужской', 'Женский', 'Мужской',
       'Мужской', 'Мужской', 'Женский', 'Мужской', 'Мужской', 'Женский', 'Мужской', 'Мужской', 'Женский', 'Мужской',
       'Мужской', 'Мужской', 'Женский', 'Женский', 'Мужской', 'Мужской', 'Женский', 'Женский', 'Мужской', 'Мужской',
       'Мужской', 'Мужской', 'Мужской', 'Женский', 'Мужской', 'Женский', 'Мужской', 'Женский', 'Женский', 'Мужской',
       'Мужской', 'Женский', 'Женский', 'Мужской', 'Мужской', 'Мужской', 'Мужской', 'Мужской', 'Мужской', 'Мужской',
       'Мужской', 'Мужской']
lst = pd.DataFrame(lst)
df['пол'] = df['пол'].fillna(lst[0])
df['температура_воздуха_на_улице'] = df['температура_воздуха_на_улице'].fillna(df['среднемесячная_температура_на_улице'])
# Заполним пропуски в графе возраст медианой по группам горoда и пол.
# df['возраст'] = df['возраст'].fillna('unknown')
a = df.groupby(['пол', 'город'])['возраст'].transform(lambda x: pd.Series.median(x))
a = a.replace('unknown', None)
# Заполним оставшиеся пропуски общей медианой
b = df['возраст'].median()
a = a.fillna(b)
df['возраст'] = df['возраст'].fillna(a)
# Не будем заполнять пропуски ощущение_движения_воздуха_(bool) так  далее эти данные не используются
# Заполним данные оценка_комфорта методом интерполюции по группам
a = df.groupby(['способ_охлаждения', 'режим_при_смешанном_типе_охлаждения', 'способ_обогрева', 'климат'])['оценка_комфорта'].apply(lambda group: group.interpolate())
a = a.reset_index()
df['оценка_комфорта'] = df['оценка_комфорта'].fillna(a['оценка_комфорта'])
# У нас ещё много пропущенных значений
# Остальное заполним групповой медианной оставшиеся удалим, если их нельзя заполнит даже групповой медианой
# Это повод ставить под сомнение их точность
a = df.groupby(['способ_охлаждения', 'режим_при_смешанном_типе_охлаждения', 'климат'])['оценка_комфорта'].transform(lambda x: pd.Series.median(x))
a = a.reset_index()
df['оценка_комфорта'] = df['оценка_комфорта'].fillna(a['оценка_комфорта'])
df = df[df['оценка_комфорта'].notna()]
# Обработаем выбросы в колонке температура_воздуха_в_помещении это могло произойти из-за ошибок в измерительных приборах
H = 3 * (df['температура_воздуха_в_помещении'].quantile(q=0.75) - df['температура_воздуха_в_помещении'].quantile(q=0.25))
maxi = df['температура_воздуха_в_помещении'].quantile(q=0.75) + H
mini = df['температура_воздуха_в_помещении'].quantile(q=0.25) - H
df.loc[df['температура_воздуха_в_помещении'] > maxi, 'температура_воздуха_в_помещении'] = None
df.loc[df['температура_воздуха_в_помещении'] < mini, 'температура_воздуха_в_помещении'] = None
a = df.groupby(['климат', 'способ_охлаждения', 'режим_при_смешанном_типе_охлаждения', 'способ_обогрева'])['температура_воздуха_в_помещении'].transform(lambda x: pd.Series.median(x))
df['температура_воздуха_в_помещении'] = df['температура_воздуха_в_помещении'].fillna(a)
# Обработаем выброся в графе скорость_воздуха они могли возникнуть из-за урагана это слишком большие значения
H = 1.5 * (df['скорость_воздуха'].quantile(q=0.75) - df['скорость_воздуха'].quantile(q=0.25))
maxi = df['скорость_воздуха'].quantile(q=0.75) + H
mini = df['скорость_воздуха'].quantile(q=0.25) - H
df.loc[df['скорость_воздуха'] > maxi, 'скорость_воздуха'] = None
df.loc[df['скорость_воздуха'] < mini, 'скорость_воздуха'] = None
a = df.groupby(['климат', 'способ_охлаждения', 'режим_при_смешанном_типе_охлаждения'])['скорость_воздуха'].transform(lambda x: pd.Series.median(x))
df['скорость_воздуха'] = df['скорость_воздуха'].fillna(a)
# Обработаем выброся в графе среднемесячная_температура_на_улице они могли возникнуть из-за ошибки ввода или прибора
H = 3 * (df['среднемесячная_температура_на_улице'].quantile(q=0.75) - df['среднемесячная_температура_на_улице'].quantile(q=0.25))
maxi = df['среднемесячная_температура_на_улице'].quantile(q=0.75) + H
mini = df['среднемесячная_температура_на_улице'].quantile(q=0.25) - H
df.loc[df['среднемесячная_температура_на_улице'] > maxi, 'среднемесячная_температура_на_улице'] = None
df.loc[df['среднемесячная_температура_на_улице'] < mini, 'среднемесячная_температура_на_улице'] = None
a = df.groupby(['климат', 'способ_охлаждения', 'режим_при_смешанном_типе_охлаждения'])['среднемесячная_температура_на_улице'].transform(lambda x: pd.Series.median(x))
df['среднемесячная_температура_на_улице'] = df['среднемесячная_температура_на_улице'].fillna(a)
# Обработаем дубликаты
dub_by = ['способ_охлаждения', 'режим_при_смешанном_типе_охлаждения', 'ощущение_температуры',
          'предпочтительное_изменение_температуры', 'предпочтительное_изменение_движения_воздуха',
          'способ_обогрева', 'rh']
df = df.drop_duplicates(subset=dub_by)
df['способ_охлаждения_без_смешанного'] = df['способ_охлаждения'].replace('Смешанный', None)
df['способ_охлаждения_без_смешанного'] = df['способ_охлаждения_без_смешанного'].fillna(df['режим_при_смешанном_типе_охлаждения'])
a = df.groupby(['способ_охлаждения_без_смешанного'])[['температура_воздуха_в_помещении','rh']].median()
df.loc[(df['rh'] >= 40) & (df['rh'] <= 60), 'влажность_воздуха'] = 'Влажность в пределах рекомендуемой'
df.loc[(df['rh'] > 30) & (df['rh'] < 40), 'влажность_воздуха'] = 'Влажность ниже рекомендуемой'
df.loc[(df['rh'] > 60) & (df['rh'] < 70), 'влажность_воздуха'] = 'Влажность выше рекомендуемой'
df.loc[df['rh'] >= 70, 'влажность_воздуха'] = 'Слишком высокая влажность'
df.loc[df['rh'] <= 30, 'влажность_воздуха'] = 'Слишком низкая влажность'
print(df[['rh', 'влажность_воздуха']])


#создание доп.категориального столбца по количеству рекламаций
df['количество_рекламаций_доп'] = df['количество_рекламаций'].apply(lambda x: 'мало' if x <= 1 else ('средне' if x == 2 else 'много'))

#создание категориального столбца по категориям возраста
df['категория_возраста'] = df['возраст'].apply(lambda x: 'молодой' if x <= 44 else ('средний' if 45 <= x <= 59 else 'пожилой'))

#расчет среднего возраста по полу
df_average_age_sex = df.groupby(['пол'])['возраст'].mean()
print(df_average_age_sex)

#расчет среднего возраста по стране
df_average_age_country = df.groupby(['страна'])['возраст'].mean()
print(df_average_age_country)

#расчет средней комфортной температуры в зависимости от возрастной категории
df_average_comf_temp_age = df[df['предпочтительное_изменение_температуры'] == 'Без изменений'].groupby(['категория_возраста'])['температура_воздуха_в_помещении'].mean()
print(df_average_comf_temp_age)
